import time
import requests
import logging
from datetime import datetime
from threading import Thread

URL = "http://127.0.0.1:8080/timestamp/"

logging.basicConfig(
    filename="timestamp.log", filemode="w",
    format="%(threadName)s %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def get_stamp():
    for i in range(20):
        current_time = datetime.now().timestamp()
        my_reg = requests.get(URL + str(current_time))
        if my_reg.status_code == 200:
            logger.info(f"{current_time} {my_reg.text}")
        time.sleep(1)


if __name__ == "__main__":
    start = time.time()
    threads = [Thread(target=get_stamp) for i in range(10)]
    for thread in threads:
        thread.start()
        time.sleep(1)
    for thread in threads:
        thread.join()
    print(f"Время выполнения {time.time() - start}")