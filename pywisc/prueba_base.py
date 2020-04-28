import logging


logger = logging.getLogger(__name__)


class Prueba:
    """ grupos de sub-pruebas """
    def __init__(self, name=None, code=None):
        self.name = name
        self.code = code
        self.subpruebas = []

    def load_from_dict(self, data):
        self.name = data['name']
        self.code = data['code']
        for subprueba in data['subtests']:
            s = SubPrueba()
            s.load_from_dict(prueba=self, data=subprueba)
            self.subpruebas.append(s)


class SubPrueba:
    """ cada una de las sub-pruebas """
    def __init__(self, prueba=None, name=None, code=None, mandatory=None, orden=0):
        self.prueba = prueba
        self.name = name
        self.code = code
        self.mandatory = mandatory
        self.orden = orden
    
    def load_from_dict(self, prueba, data):
        self.prueba = prueba
        self.name = data['name']
        self.code = data['code']
        self.orden = data['orden']
        self.mandatory = data['mandatory']
        