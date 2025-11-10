import queue
import random
import threading
import logging
import time


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def random_sleep():
    time.sleep(random.randint(1, 5))


class Task:
    def __init__(self, priority, description):
        self.priority = priority
        self.description = description


TASKS = [Task(0, "задача 0"), Task(100, "задача 1"),
         Task(25, "задача 2"), Task(75, "задача 3")]


class Producer(threading.Thread):
    def __init__(self, que: queue.PriorityQueue):
        super().__init__()
        self.queue = que

    def run(self):
        logger.info("Producer Добавляет задачи в очередь")
        for task in TASKS:
            self.queue.put((task.priority, task))
        logger.info("Producer: Все задачи добавлены ")


class Consumer(threading.Thread):
    def __init__(self, que: queue.PriorityQueue):
        super().__init__()
        self.queue = que

    def run(self):
        logger.info(f"Consumer: Выполнение поставленных задач из очереди")
        while True:
            start = time.time()
            priority, task = self.queue.get()
            random_sleep()
            logger.info(f"Выполняется {task.description} с приоритетом {priority}, sleep({time.time() - start})")
            if self.queue.empty():
                break
        logger.info(f"Consumer Все задачи выполнены")


def main():
    general_queue = queue.PriorityQueue()
    producer = Producer(general_queue)
    consumer = Consumer(general_queue)
    producer.start()
    consumer.start()
    producer.join()
    consumer.join()


if __name__ == "__main__":
    main()