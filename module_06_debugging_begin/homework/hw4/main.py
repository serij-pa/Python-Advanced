"""
Ваш коллега, применив JsonAdapter из предыдущей задачи, сохранил логи работы его сайта за сутки
в файле skillbox_json_messages.log. Помогите ему собрать следующие данные:

1. Сколько было сообщений каждого уровня за сутки.
2. В какой час было больше всего логов.
3. Сколько логов уровня CRITICAL было в период с 05:00:00 по 05:20:00.
4. Сколько сообщений содержит слово dog.
5. Какое слово чаще всего встречалось в сообщениях уровня WARNING.
"""
import json
import shlex
import subprocess
from collections import defaultdict
from itertools import count
from os.path import split
from typing import Dict

#from module_05_processes_and_threads.homework.hw5_add.self_printing import result


def task1() -> Dict[str, int]:
    """
    1. Сколько было сообщений каждого уровня за сутки.
    @return: словарь вида {уровень: количество}
    """
    with open("skillbox_json_messages.log", "r") as file:
        lines = file.readlines()

    result = defaultdict(dict)

    for line in lines:
        res_line = line.split()[3][1:][:-2]

        if res_line in result:
            result[res_line] += 1
        else:
            result[res_line] = 1

    result1 = defaultdict(dict)
    level_list = ["INFO", "WARNING", "DEBUG", "ERROR", "CRITICAL"]
    for level in level_list:
        cmd = f"""grep -c '"level": "{level}"' skillbox_json_messages.log"""
        num_level = subprocess.run([cmd],
                                   shell=True,
                                   stdout=subprocess.PIPE).stdout.decode()
        result1[level] = int(num_level)

    return dict(result), dict(result1)


def task2() -> int:
    """
    2. В какой час было больше всего логов.
    @return: час
    """
    result = {}
    for time in range(0,24):
        if time < 10:
            cmd = f"""grep -c '"time": "0{time}:[0-1][0-9]:[0-9][0-9]"' skillbox_json_messages.log"""
            count_log1  = subprocess.run([cmd], shell=True, stdout=subprocess.PIPE).stdout.decode()
            result[time] = (int(count_log1))
        else:
            cmd = f"""grep -c '"time": "{time}:[0-1][0-9]:[0-9][0-9]"' skillbox_json_messages.log"""
            count_log = subprocess.run([cmd], shell=True, stdout=subprocess.PIPE).stdout.decode()
            result[time] = (int(count_log))

    for key, val in result.items():
        if val == max(result.values()):
            max_key = key

    return f"С {max_key} по {int(max_key) + 1} max_log = {max(result.values())}"


def task3() -> int:
    """
    3. Сколько логов уровня CRITICAL было в период с 05:00:00 по 05:20:00.
    @return: количество логов
    """
    cmd = f"""grep -c '"time": "05:[0-1][0-9]:[0-9][0-9]", "level": "CRITICAL"' skillbox_json_messages.log"""
    result = subprocess.run([cmd],
                               shell=True,
                               stdout=subprocess.PIPE).stdout.decode()
    return f"c 05:00 по 05:20 было {int(result)} логов"


def task4() -> int:
    """
    4. Сколько сообщений содержат слово dog.
    @return: количество сообщений
    """
    cmd = f"""grep -c 'dog' skillbox_json_messages.log"""
    result = subprocess.run(cmd,
                            shell=True,
                            stdout=subprocess.PIPE).stdout.decode()
    return f"слово dog встречается {int(result)} раз"


def task5() -> str:
    """
    5. Какое слово чаще всего встречалось в сообщениях уровня WARNING.
    @return: слово
    """
    count = 0
    count_word = defaultdict(dict)
    with open("skillbox_json_messages.log", "r") as file:
        lines = file.readlines()
    for line in lines:
        dict_line = json.loads(line)

        if dict_line["level"] == "WARNING":
            for word in (dict_line["message"]).split():
                if word in count_word:
                    count_word[word] += 1
                else:
                    count_word[word] = 1
    max_word = []
    for key, val in count_word.items():
        #print(val)
        if val == max(count_word.values()):
            max_word.append(key)


    return f"Слова {max_word} встречатся {max(count_word.values())} раз"




if __name__ == '__main__':
    tasks = (task1, task2, task3, task4, task5)
    for i, task_fun in enumerate(tasks, 1):
        task_answer = task_fun()
        print(f'{i}. {task_answer}')
