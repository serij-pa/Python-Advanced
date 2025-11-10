"""
Реализуйте контекстный менеджер, который будет игнорировать переданные типы исключений, возникающие внутри блока with.
Если выкидывается неожидаемый тип исключения, то он прокидывается выше.
"""
import sys
from typing import Collection, Type, Literal
from types import TracebackType


class BlockErrors:
    def __init__(self, errors: Collection) -> None:
        self.errors = errors

    def __enter__(self) -> None:
        pass

    def __exit__(
            self,
            exc_type: Type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None
    ) -> Literal[True] | None:
        if exc_type is not None and issubclass(exc_type, tuple(self.errors)):
        #if issubclass(exc_type, tuple(self.errors)) and exc_type in self.errors:
            return True





def example_1():
    err_types = {ZeroDivisionError, TypeError}
    with BlockErrors(err_types):
        a = 1 / 0
    print('Выполнено без ошибок')


def example_2():
    err_types = {ZeroDivisionError}
    with BlockErrors(err_types):
        a = 1 / '0'
    print('Выполнено без ошибок')


def example_3():
    outer_err_types = {TypeError}
    with BlockErrors(outer_err_types):
        inner_err_types = {ZeroDivisionError}
        with BlockErrors(inner_err_types):
            a = 1 / '0'
        print('Внутренний блок: выполнено без ошибок')
    print('Внешний блок: выполнено без ошибок')


def example_4():
    err_types = {Exception}
    with BlockErrors(err_types):
        a = 1 / '0'
    print('Выполнено без ошибок')


