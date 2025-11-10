import logging
import sys
from utils2 import string_to_operator


logger = logging.getLogger("app2")
logger.setLevel("INFO")
formatter = logging.Formatter(fmt="%(levelname)s | %(name)s | %(asctime)s | %(lineno)s |%(message)s")
custom_handler = logging.StreamHandler()
custom_handler.setFormatter(formatter)
logger.addHandler(custom_handler)


def calc(args):
    logger.info(f"Arguments:  {args}")

    num_1 = args[0]
    operator = args[1]
    num_2 = args[2]

    try:
        num_1 = float(num_1)
    except ValueError as e:
        logger.error("Error while converting number 1")
        logger.error(e)

    try:
        num_2 = float(num_2)
    except ValueError as e:
        logger.error("Error while converting number 2")
        logger.error(e)

    operator_func = string_to_operator(operator)

    result = operator_func(num_1, num_2)

    logger.info(f"Result: , {result}")
    logger.info(f"{num_1} {operator} {num_2} = {result}")


if __name__ == '__main__':
    # calc(sys.argv[1:])
    calc('2+5')
