from pywisc.wisc_base import Wisc


def test_01():
    df = 'pywisc/data/wisc_4_es_ar.json'
    w = Wisc(definition_data=df)
    assert w.is_valid