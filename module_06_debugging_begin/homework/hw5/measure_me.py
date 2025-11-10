"""
Каждый лог содержит в себе метку времени, а значит, правильно организовав логирование,
можно отследить, сколько времени выполняется функция.

Программа, которую вы видите, по умолчанию пишет логи в stdout. Внутри неё есть функция measure_me,
в начале и в конце которой пишется "Enter measure_me" и "Leave measure_me".
Сконфигурируйте логгер, запустите программу, соберите логи и посчитайте среднее время выполнения функции measure_me.
"""
import logging
import random
import json
import subprocess
import datetime
from typing import List

logger = logging.getLogger(__name__)


def get_data_line(sz: int) -> List[int]:
    try:
        logger.debug("Enter get_data_line")
        return [random.randint(-(2 ** 31), 2 ** 31 - 1) for _ in range(sz)]
    finally:
        logger.debug("Leave get_data_line")


def measure_me(nums: List[int]) -> List[List[int]]:
    logger.debug("Enter measure_me")
    results = []
    nums.sort()

    for i in range(len(nums) - 2):
        logger.debug(f"Iteration {i}")
        left = i + 1
        right = len(nums) - 1
        target = 0 - nums[i]
        if i == 0 or nums[i] != nums[i - 1]:
            while left < right:
                s = nums[left] + nums[right]
                if s == target:
                    logger.debug(f"Found {target}")
                    results.append([nums[i], nums[left], nums[right]])
                    logger.debug(
                        f"Appended {[nums[i], nums[left], nums[right]]} to result"
                    )
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    left += 1
                    right -= 1
                elif s < target:
                    logger.debug(f"Increment left (left, right) = {left, right}")
                    left += 1
                else:
                    logger.debug(f"Decrement right (left, right) = {left, right}")

                    right -= 1

    logger.debug("Leave measure_me")

    return results


def count_measure_me():
    #cmd = f"""grep -c '"message": "Enter measure_me"' list_logs.txt"""
    #num_level = subprocess.run([cmd], shell=True, stdout=subprocess.PIPE).stdout.decode()
    #print(int(num_level))

    message_enter = "Enter measure_me"
    message_leave = "Leave measure_me"
    time_enter = []
    time_leave = []
    with open("list_logs.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            if message_enter in line:
                dict_line = json.loads(line)
                num = (datetime.datetime.strptime((dict_line["time"]), "%Y-%m-%d %H:%M:%S,%f").timestamp())
                time_enter.append(num)
            elif message_leave in line:
                dict_line = json.loads(line)
                num = (datetime.datetime.strptime((dict_line["time"]), "%Y-%m-%d %H:%M:%S,%f").timestamp())
                time_leave.append(num)
    time_work = list(map(lambda x, y: y - x, time_enter, time_leave))
    len_list = len(time_work)
    average_time = sum(time_work) / len_list

    return f"среднее время выполнения функции measure_me {round(average_time, 5)}"


if __name__ == "__main__":
    logging.basicConfig(level="DEBUG",
                        format=json.dumps({"time": "%(asctime)s", "level": "%(levelname)s", "message": '%(message)s'}),
                        #datefmt='%H:%M:%S',
                        filename="list_logs.txt")
    for it in range(15):
        #data_line = get_data_line(10 ** 3) #первичный
        data_line = get_data_line(3 ** 3)
        measure_me(data_line)
    print(count_measure_me())
