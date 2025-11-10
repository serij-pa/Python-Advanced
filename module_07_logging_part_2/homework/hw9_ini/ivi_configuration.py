import logging.config
from dict_config import dict_config

logging.config.dictConfig(dict_config)
logger = logging.getLogger("appLogger")



logger.debug("level DDEBUG")
logger.info("level INFO")
logger.warning("level WARNING")

