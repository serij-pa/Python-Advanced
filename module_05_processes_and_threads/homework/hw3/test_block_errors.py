import unittest
from block_errors import BlockErrors

class TestBlockErrors(unittest.TestCase):

    def setUp(self):
        pass

    def test_example_1(self):
        err_types = {ZeroDivisionError, TypeError}
        with BlockErrors(err_types):
            a = 1 / 0
        print('Выполнено без ошибок')

    def test_example_2(self):
        err_types = {ZeroDivisionError}
        with BlockErrors(err_types):
            a = 1 / '0'
        print('Выполнено без ошибок')

    def test_example_3(self):
        outer_err_types = {TypeError}
        with BlockErrors(outer_err_types):
            inner_err_types = {ZeroDivisionError}
            with BlockErrors(inner_err_types):
                a = 1 / '0'
            print('Внутренний блок: выполнено без ошибок')
        print('Внешний блок: выполнено без ошибок')

    def test_example_4(self):
        err_types = {Exception}
        with BlockErrors(err_types):
            a = 1 / '0'
        print('Выполнено без ошибок')


if __name__ == '__main__':
    unittest.main()
