import logging
import logging.config
from typing import Union, Callable
from operator import sub, mul, truediv, add
from config_file import dict_config



OPERATORS = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': truediv,
}

Numeric = Union[int, float]
#logging.basicConfig(level="DEBUG")
logging.config.dictConfig(dict_config)
logger = logging.getLogger("module_logger.logger")
logger.setLevel("DEBUG")


def string_to_operator(value: str) -> Callable[[Numeric, Numeric], Numeric]:
    """
    Convert string to arithmetic function
    :param value: basic arithmetic function
    """
    if not isinstance(value, str):
        #print("wrong operator type", value)
        logger.error(f"wrong operator type {value}")
        raise ValueError("wrong operator type")

    if value not in OPERATORS:
        #print("wrong operator value", value)
        logger.error(f"wrong operator value {value}")
        raise ValueError("wrong operator value")

    return OPERATORS[value]
