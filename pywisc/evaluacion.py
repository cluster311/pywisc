import json
import logging
from datetime import datetime
from pywisc.tools.csv_drive import DriveCSV


logger = logging.getLogger(__name__)


class Evaluacion:
    """ Evaluacion de cada uno de los niñes evaluados """

    def __init__(self, wisc):
        """ Inicializacion
            Params:
                wisc = Version específica de WISC a usar
        """
        self.wisc = wisc

        # todos los datos cargados
        self.data = {}

        # indice de datos para transformacion a escalares
        self.escalares = self.load_escalares()
        # elegir la tabla solo cuando sepa cuantos meses tiene
        self.tabla_escalar = {}
    
    def calculate_age(self):
        born_date = self.data['born_date']
        test_date = self.data['test_date']

        full_months = (test_date.year - born_date.year) * 12 + test_date.month - born_date.month
        years = full_months // 12
        months = full_months % 12
        print(f'Total meses: {full_months}')
        print(f'o {years} años y and {months}')
        self.data['full_months'] = full_months
        self.data['years'] = years
        self.data['months'] = months

    def load_escalares(self):
        """ cargar los datos de paso de directa a escalar correspondiente a la edad """
        ver = self.wisc.version
        lang = self.wisc.language
        df = f'pywisc/data/data_{ver}_{lang}.json'
        f = open(df, 'r')
        data = json.loads(f.read())
        f.close()
        return data
    
    def get_escalar_table(self):
        """ encontrar cual de todas las tablas de escalares corresponde con la edad del paciente """

        meses = self.data['full_months']
        for esc in self.escalares:
            if meses >= esc['from_months']:
                if meses <= esc['to_months']:
                    return esc
        raise ValueError(f'No se encontro la tabla de escalares para un paciente de {meses} meses')
        
    
    def start_as_terminal(self):
        """ ask required data to start """
        rts = self.wisc.required_to_start
        
        for req in rts:
            text = req['text']
            fts = req['formats_txt_to_user']
            ask = f'{text} \n\tFormato: {fts}\n'
            if req['default'] is not None:
                if req['default'] == 'today':
                    dft = datetime.today().strftime("%Y-%m-%d")
                ask += f'\tPredeterminado: {dft}\n'
            
            s = input(ask)
            if s == '':
                if req['default'] is not None:
                    s = dft
                else:
                    raise ValueError('Debes completar el dato')
            
            if req['data_type'] == 'date':
                val = None
                for fmt in req['formats']:
                    try:
                        val = datetime.strptime(s, fmt)
                    except ValueError:
                        pass
                    if val is not None:
                        break

                if val is None:
                    raise ValueError('No coincide con ninguno de los formatos esperados')
        
                self.data[req['code']] = val

        self.calculate_age()
        self.tabla_escalar = self.get_escalar_table()
        code = self.tabla_escalar['code']
        uid = self.tabla_escalar['drive_uid']
        gid = self.tabla_escalar['drive_gid']
        drive_name = f'wisc-{self.wisc.version}-{self.wisc.language}-{self.wisc.country}-{code}'
        d = DriveCSV(name=drive_name,
                 unique_id_column='Escalar',
                 uid=uid, gid=gid)
        escalares = d.tree
        print(escalares)

        # tomar las puntuaciones directas y trasformarlas en escalares
        self.data['escalares'] = {}
        for prueba in self.wisc.pruebas:
            # solo espero un numero entero por cada subtest
            for subprueba in prueba.subpruebas:
                name = '{}-{}'.format(prueba.name, subprueba.name)
                code = '{}-{}'.format(prueba.code, subprueba.code)
                
                if not subprueba.mandatory:
                    print(f'Ignorando la prueba no obligatoria {name}')
                    continue

                ask = f'{name} ({code}):'
                directa = int(input(ask))
                escalar = None
                for row in escalares:
                    # TODO deben estar ordenados
                    if row[subprueba.code] != '':
                        val = int(row[subprueba.code])
                        print(f'{val} vs {directa}')
                        if val >= directa:
                            escalar = int(row['Escalar'])
                            break
                if escalar is None:
                    raise ValueError(f'No se encontró el escalar para la directa={directa} para {code}')
                
                d = {'directa': directa, 'escalar': escalar}
                self.data['escalares'][code] = d
                print(f'{code}: {d}')
        
        # sumar escalares
        ci = 0
        for code, esc in self.data['escalares'].items():
            ci += esc['escalar']
        print(f'CI: {ci}')
        
        # TODO test: con 10 en todas las directas el CI es 89