from pywisc.evaluacion import Evaluacion
from pywisc.wisc import Wisc


def main():
    print("##########################")
    print("Calculador WISC 4. Versión español, Argentina")
    print("##########################")
    df = 'pywisc/data/wisc_4_es_ar.json'
    w = Wisc(definition_data=df)
    e = Evaluacion(wisc=w)
    e.ask_directas_as_terminal()