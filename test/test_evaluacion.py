from pywisc.wisc import Wisc
from pywisc.evaluacion import Evaluacion

def evaluate(directas, born_date, test_date, wisc_version=4, language='es', country='ar'):
    """ evalua wisc, devuleve el CI """
    w = Wisc(wisc_version=wisc_version,
             language=language,
             country=country)
    e = Evaluacion(wisc=w)
    reqs = {'born_date': born_date, 'test_date': test_date}
    e.validate_reqs(reqs=reqs)
    e.calculate_age()
    return e.calculate_ci(directas=directas)


# ##################################################
# 6 años y 0-3 meses
# ##################################################

def test_evaluacion_10_6_0():
    data =  {'S': 10, 'V': 10, 'C': 10, 'CC': 10,
             'Co': 10, 'M': 10, 'RD': 10, 'LN': 10,
             'Cl': 10, 'BS': 10}
    ci = evaluate(directas=data, born_date='2014-03-01', test_date='2020-04-29')
    assert ci == 89


def test_evaluacion_15_6_0():
    data =  {'S': 15, 'V': 15, 'C': 15, 'CC': 15,
             'Co': 15, 'M': 15, 'RD': 15, 'LN': 15,
             'Cl': 15, 'BS': 15}
    ci = evaluate(directas=data, born_date='2014-03-01', test_date='2020-04-29')
    assert ci == 123


def test_evaluacion_20_6_0():
    data =  {'S': 20, 'V': 20, 'C': 20, 'CC': 20,
             'Co': 20, 'M': 20, 'RD': 20, 'LN': 20,
             'Cl': 20, 'BS': 20}
    ci = evaluate(directas=data, born_date='2014-03-01', test_date='2020-04-29')
    assert ci == 151

# ##################################################
# 15 años y 0-3 meses
# ##################################################


def test_evaluacion_15_0_A():
    data =  {'CC': 28, 'S': 17,'RD': 11, 'Co': 14, 'Cl': 43, 'V': 36, 'LN': 14, 'M': 16, 'C': 20, 'BS': 19}
    ci = evaluate(directas=data, born_date='2005-05-01', test_date='2020-05-13')
    assert ci == 50


def test_evaluacion_15_1_B():
    data =  {'CC': 47, 'S': 27,'RD': 17, 'Co': 20, 'Cl': 63, 'V': 47, 'LN': 19, 'M': 25, 'C': 31, 'BS': 31}
    ci = evaluate(directas=data, born_date='2005-03-01', test_date='2020-05-13')
    assert ci == 100


def test_evaluacion_15_2_C():
    data =  {'CC': 63, 'S': 39,'RD': 25, 'Co': 24, 'Cl': 79, 'V': 59, 'LN': 24, 'M': 31, 'C': 38, 'BS': 42}
    ci = evaluate(directas=data, born_date='2005-02-01', test_date='2020-05-13')
    assert ci == 150


# ##################################################
# 14 años y 8-11 meses
# ##################################################


def test_evaluacion_14_8():
    data =  {'CC': 28, 'S': 17,'RD': 11, 'Co': 14, 'Cl': 40, 'V': 33, 'LN': 14, 'M': 16, 'C': 20, 'BS': 20}
    ci = evaluate(directas=data, born_date='2005-09-01', test_date='2020-05-13')
    assert ci == 50


def test_evaluacion_14_9():
    data =  {'CC': 47, 'S': 27,'RD': 17, 'Co': 20, 'Cl': 61, 'V': 48, 'LN': 19, 'M': 25, 'C': 31, 'BS': 31}
    ci = evaluate(directas=data, born_date='2005-08-01', test_date='2020-05-13')
    assert ci == 101


def test_evaluacion_14_10():
    data =  {'CC': 63, 'S': 40,'RD': 23, 'Co': 25, 'Cl': 80, 'V': 60, 'LN': 24, 'M': 31, 'C': 39, 'BS': 42}
    ci = evaluate(directas=data, born_date='2005-07-01', test_date='2020-05-13')
    assert ci == 159


# ##################################################
# 14 años y 4-7 meses
# ##################################################


def test_evaluacion_14_4():
    data =  {'CC': 26, 'S': 17,'RD': 11, 'Co': 14, 'Cl': 37, 'V': 30, 'LN': 14, 'M': 17, 'C': 20, 'BS': 10}
    ci = evaluate(directas=data, born_date='2006-01-01', test_date='2020-05-13')
    assert ci == 46


def test_evaluacion_14_5():
    data =  {'CC': 68, 'S': 27,'RD': 17, 'Co': 20, 'Cl': 57, 'V': 47, 'LN': 19, 'M': 25, 'C': 31, 'BS': 31}
    ci = evaluate(directas=data, born_date='2005-12-01', test_date='2020-05-13')
    assert ci == 112


def test_evaluacion_14_6():
    data =  {'CC': 60, 'S': 44,'RD': 22, 'Co': 24, 'Cl': 77, 'V': 58, 'LN': 23, 'M': 30, 'C': 38, 'BS': 40}
    ci = evaluate(directas=data, born_date='2005-11-01', test_date='2020-05-13')
    assert ci == 154


