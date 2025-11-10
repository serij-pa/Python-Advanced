import logging
import threading
import time
from concurrent.futures import ThreadPoolExecutor


logging.basicConfig(level='INFO')
logger: logging.Logger = logging.getLogger(__name__)


class Forks:
    lock = threading.Lock()
    free_fork = []

    def __init__(self):
        for x in range(5):
            self.free_fork.append(True)


class Philosopher():
    def __init__(self, name, num, forks):
        self.name = name
        self.num = num
        self.forks = forks

    def condition(self):
        while True:
            logger.info(f'Philosopher {self.name} начало размышлений.')
            time.sleep(4)
            logger.info(f'Philosopher {self.name} проголодался, берет вилку')
            with forks.lock:
                if self.forks.free_fork[self.num] is True and \
                        self.forks.free_fork[(self.num + 1) % 5] is True:
                    self.forks.free_fork[self.num] = False
                    self.forks.free_fork[(self.num + 1) % 5] = False
                    logger.info(f'Philosopher {self.name} начинает КУШАТЬ.')
                    time.sleep(5)
                    logger.info(f'Philosopher {self.name} заканчивает КУШАТЬ и откладывает вилку.')
                    self.forks.free_fork[self.num] = False
                    self.forks.free_fork[(self.num + 1) % 5] = False


if __name__ == "__main__":
    #Сократ, Аристотель, Кант, Гегель, Ницше, Фрейд
    forks = Forks()
    with ThreadPoolExecutor(max_workers=5) as exp:
        philosophers = [
            Philosopher("Сократ", 1, forks),
            Philosopher("Аристотель", 2, forks),
            Philosopher("Кант", 3, forks),
            Philosopher("Гегель", 4, forks),
            Philosopher("Ницше", 0, forks),
        ]
        for philosopher in philosophers:
            exp.submit(philosopher.condition)
