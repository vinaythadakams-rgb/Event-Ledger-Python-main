import logging
from logging.handlers import RotatingFileHandler

LOG_FILE = "event_ledger.log"
LOG_LEVEL = logging.INFO

def setup_logging() -> None:
    formatter = logging.Formatter(
        '{"timestamp":"%(asctime)s","level":"%(levelname)s","logger":"%(name)s","message":"%(message)s"}'
    )

    handler = RotatingFileHandler(LOG_FILE, maxBytes=5_000_000, backupCount=2)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(LOG_LEVEL)
    if not root_logger.handlers:
        root_logger.addHandler(handler)
    else:
        for existing in list(root_logger.handlers):
            root_logger.removeHandler(existing)
        root_logger.addHandler(handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
