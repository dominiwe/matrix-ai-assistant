from logbook import Logger, StreamHandler
import sys
from .log import logger_group

logger = Logger("bot.main")
logger_group.add_logger(logger)

StreamHandler(sys.stdout).push_application()

logger.debug("Application entrypoint.")

from .config import config
from . import db
from .bot import bot

def main():
    # Starting up
    logger.info(f"""Bot is in {'prod' if config.get("production") else 'dev'} mode!""")
    bot.run()