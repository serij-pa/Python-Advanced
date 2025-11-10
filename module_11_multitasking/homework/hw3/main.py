import logging
import random
import threading
import time
from typing import List

TOTAL_TICKETS: int = 100
DIRECTOR_TICKET = 10

logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)


class Director(threading.Thread):
    def __init__(self, semaphore: threading.Semaphore):
        super(Director, self).__init__()
        self.lock: threading.Semaphore = semaphore
        logger.info("Директор добавляет билеты")

    def run(self):
        global TOTAL_TICKETS, DIRECTOR_TICKET
        while TOTAL_TICKETS:
            if DIRECTOR_TICKET < 4:
                with self.lock:
                    added_tickets = 10 - DIRECTOR_TICKET % 10
                    if added_tickets > TOTAL_TICKETS:
                        added_tickets = TOTAL_TICKETS
                    DIRECTOR_TICKET += added_tickets
                    TOTAL_TICKETS -= added_tickets
                    logger.info(f"Директор добавил {added_tickets} билетов")

        logger.info(f"Директор остановил работу билеты распроданы")


class Seller(threading.Thread):

    def __init__(self, semaphore: threading.Semaphore) -> None:
        super().__init__()
        self.sem: threading.Semaphore = semaphore
        self.tickets_sold: int = 0
        logger.info('Продавец приступил к работе')

    def run(self) -> None:
        global TOTAL_TICKETS
        is_running: bool = True
        while is_running:
            self.random_sleep()
            with self.sem:
                if TOTAL_TICKETS <= 0:
                    break
                self.tickets_sold += 1
                TOTAL_TICKETS -= 1
                logger.info(f'{self.name} sold one;  {TOTAL_TICKETS} left')
        logger.info(f'Seller {self.name} sold {self.tickets_sold} tickets')

    def random_sleep(self) -> None:
        time.sleep(random.randint(0, 1))


def main() -> None:
    semaphore: threading.Semaphore = threading.Semaphore()

    director = Director(semaphore=semaphore)
    director.start()

    sellers: List[Seller] = [director]
    for _ in range(4):
        seller = Seller(semaphore)
        seller.start()
        sellers.append(seller)

    for seller in sellers:
        seller.join()


if __name__ == '__main__':
    main()
