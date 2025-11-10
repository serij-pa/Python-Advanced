
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
            "formatter": "base"
        },
        "hand_http": {
            "class": "logging.handlers.HTTPHandler",
            "formatter": "base",
            "level": "DEBUG",
            "host": "127.0.0.1:5000",
            "url": "/log",
            "method": "POST"}
    },
    "loggers": {
        "module_logger": {
            "level": "DEBUG",
            "handlers": ["console", "hand_http", ]
            #"handlers": ["console", ]
            # "propagate": False,
        }
    },

    # "filters": {},
    # "root": {} # == "": {}
}