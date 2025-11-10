import logging
import logging.config
import sys


class LevelFileHandler(logging.Handler):

    def __init__(self, file_name, mode='a'):
        super().__init__()
        self.file_name = file_name
        self.mode = mode


    def emit(self, record: logging.LogRecord) -> None:
        message = self.format(record)

        if record.levelname == "DEBUG":
            self.file_name = "calc_debug.log"
        elif record.levelname == "ERROR":
            self.file_name = "calc_error.log."

        with open(self.file_name, mode=self.mode) as f:
            f.write(message + '\n')


def get_logger(name):
    logging.basicConfig(
        format="%(levelname)s | %(name)s | %(message)s",
        level="DEBUG",
        handlers=[LevelFileHandler(file_name="customlogfile.log"), logging.StreamHandler()]
    )
    logger = logging.getLogger(f"my_logger.{name}")
    return logger

