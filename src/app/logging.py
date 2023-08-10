import json
import logging
import logging.config

from asgi_correlation_id.log_filters import correlation_id_filter

log_level_map = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
}

log_format = (
    "[%(asctime)s] [%(levelname)s] [%(module)s] [%(correlation_id)s] %(message)s"
)
log_formatter = logging.Formatter(log_format)


def setup_logging(log_level: str, log_location: str) -> None:
    from app import config

    if log_location == "cloud":
        with open(config.settings.log_config, "r") as log_config:
            config = json.load(log_config)
            config["filters"]["correlation_id"]["()"] = correlation_id_filter(
                uuid_length=32
            )
            logging.config.dictConfig(config)
    elif not logging.root.hasHandlers():
        global_stream = logging.StreamHandler()
        global_stream.setFormatter(log_formatter)
        logging.root.addHandler(global_stream)

    level = log_level_map[log_level]
    logging.getLogger("code-challenge").setLevel(level)
    logging.root.setLevel(level)
