from benedict import benedict
import logbook
from dotenv import load_dotenv
from os import environ as env, path
from .log import logger_group

logger = logbook.Logger("bot.config")
logger_group.add_logger(logger)

config = benedict({
    # Default config
    "production": False,
})

logger.debug("Starting to load and validate config!")

# Validate env variables
def _validate_env():
    
    # Turn .env file into env variables
    load_dotenv()

    # Check if prod or dev mode
    prod = env.get("PRODUCTION")
    if prod and prod in ["true", "True", 1]:
        # In production mode
        config.set("production", True)
        logger_group.level = logbook.CRITICAL

    # Configure log level if set
    log_level = env.get("LOG_LEVEL")
    if log_level:
        if log_level == "DEBUG":
            log_level = logbook.DEBUG
        elif log_level == "INFO":
            log_level = logbook.INFO
        elif log_level == "WARNING":
            log_level = logbook.WARNING
        elif log_level == "ERROR":
            log_level = logbook.ERROR
        elif log_level == "CRITICAL":
            log_level = logbook.CRITICAL
        config.set("log_level", log_level)
        logger_group.level = log_level

    config_options = {
        "homeserver": env.get("MATRIX_HOMESERVER"),
        "username": env.get("MATRIX_BOT_USERNAME"),
        "openai_key": env.get("OPENAI_API_KEY"),
        "access_token": env.get("MATRIX_ACCESS_TOKEN")
        }

    for option in config_options:
        if not config_options.get(option):
            logger.critical(f"Option {option} not configured... exiting.")
            exit(1)
        else:
            config.set(option, config_options.get(option))
    
    db_path = env.get("DB_PATH")
    if db_path:
        location_file = path.split(db_path)
        if path.exists(location_file[0]):
            config.set("db_location", location_file[0])
            config.set("db_file", location_file[1])
        else:
            logger.critical(f"Database location doesn't exist... exiting.")
            exit(1)

_validate_env()

logger.debug("Loaded and validated config!")