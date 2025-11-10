"""
Иногда возникает необходимость перенаправить вывод в нужное нам место внутри программы по ходу её выполнения.
Реализуйте контекстный менеджер, который принимает два IO-объекта (например, открытые файлы)
и перенаправляет туда стандартные потоки stdout и stderr.

Аргументы контекстного менеджера должны быть непозиционными,
чтобы можно было ещё перенаправить только stdout или только stderr.
"""
import sys
import traceback
from types import TracebackType
from typing import Type, Literal, IO


class Redirect:
    def __init__(self, stdout: IO = None, stderr: IO = None) -> None:
        #print("Вызов инит")
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr
        self.stdout_my = stdout
        self.stderr_my = stderr


    def __enter__(self):
        #print("Вызов энтер")
        sys.stdout = self.stdout_my
        sys.stderr = self.stderr_my


    def __exit__(
            self,
            exc_type: Type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None
    ) -> Literal[True] | None:

        if self.stderr_my:
            sys.stderr.write(traceback.format_exc())
        self.stdout_my.close()
        self.stderr_my.close()
        sys.stdout = self.old_stdout
        if self.stderr_my:
            sys.stderr = self.old_stderr
            return True


if __name__ == "__main__":
    print("Hello stdout")
    stdout_file = open("stdout.txt", "w")
    stderr_file = open("stderr.txt", "w")

    with Redirect(stdout=stdout_file, stderr=stderr_file):
        print("Hello stdout.txt")
        raise Exception("Hello stderr.txt")

    print("Hello stdout again")
    raise Exception("Hello stderr")
