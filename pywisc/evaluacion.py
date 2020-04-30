import json
import logging
from datetime import datetime
from pywisc.tools.csv_drive import DriveCSV
from pywisc.escalares import TablaEscalar


logger = logging.getLogger(__name__)


class Evaluacion:
    """ Evaluacion de cada uno de los niñes evaluados """

    def __init__(self, wisc):
        """ Inicializacion
            Params:
                wisc = Version específica de WISC a usar
        """
        self.wisc = wisc

        # todos los datos cargados de este proceso
        self.data = {}

    def calculate_age(self):
        born_date = self.data['born_date']
        test_date = self.data['test_date']

        full_months = (test_date.year - born_date.year) * 12 + test_date.month - born_date.month
        years = full_months // 12
        months = full_months % 12
        logger.info(f'Total meses: {full_months}')
        logger.info(f'o {years} años y and {months}')
        self.data['full_months'] = full_months
        self.data['years'] = years
        self.data['months'] = months        
    
    def calculate(self):
        


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
        te = TablaEscalar(wisc=self.wisc, meses=self.data['full_months'])

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
                for row in te.data:
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
        escalares = []
        for code, esc in self.data['escalares'].items():
            ci += esc['escalar']
            directa, escalar = esc['directa'], esc['escalar']
            escalares.append(f'{code}= {directa} {escalar}')
        print(f'CI calculado: {ci}')
        valores = ', '.join(escalares)
        print(f'\t valores: {valores}')
        
        # TODO test: con 10 en todas las directas el CI es 89