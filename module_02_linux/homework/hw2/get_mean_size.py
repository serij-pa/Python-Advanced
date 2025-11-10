"""
Удобно направлять результат выполнения команды напрямую в программу с помощью конвейера (pipe):

$ ls -l | python3 get_mean_size.py

Напишите функцию get_mean_size, которая на вход принимает результат выполнения команды ls -l,
а возвращает средний размер файла в каталоге.
"""

import sys


def get_mean_size(ls_output: str) -> float:
    lines = ls_output.split("\n")[1:]
    total_size = 0
    file_count = 0
    for i_lines in lines:
        if i_lines:
            file_size = int(i_lines.split()[4])
            total_size += file_size
            file_count += 1
    if file_count > 0:
        average_size = total_size / file_count
        return f"Средний размер {average_size} Б"

    return "Нет файлов"


if __name__ == '__main__':
    data: str = sys.stdin.read()
    mean_size: float = get_mean_size(data)
    print(mean_size)
