import logging


class ASCIIFilter(logging.Filter):
    def filter(self, record: logging.LogRecord):
        if record.msg.isascii():
            return True
        else:
            return False


dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
            "format": "%(levelname)s | %(name)s | %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "base",
            "filters": ["ascii_filter",],
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "base",
            "filename": "logfile.log",
            "mode": "a"
        }
    },
    "loggers": {
        "module_logger": {
            "level": "DEBUG",
            "handlers": ["console"],
            # "propagate": False,
        }
    },
    "filters": {
        "ascii_filter": {
            "()": ASCIIFilter,
        }
    },
    # "root": {} # == "": {}
}