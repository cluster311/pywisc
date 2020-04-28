from pywisc.wisc_base import Wisc


def test_01():
    df = 'test/test_wisc_01.json'
    w = Wisc(definition_data=df)
    assert w.is_valid