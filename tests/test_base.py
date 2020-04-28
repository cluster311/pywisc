from pywisc.wisc_base import Wisc


df = 'tests/test_wisc_01.json'
w = Wisc(definition_data=df)
assert w.is_valid