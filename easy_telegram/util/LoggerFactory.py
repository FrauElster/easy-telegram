import logging


def get_logger(name: str, loglevel=logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    formatter = logging.Formatter('%(levelname)s \t|%(asctime)s \t| %(name)s \t|  %(message)s')

    console_handler: logging.StreamHandler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(loglevel)

    logger.setLevel(loglevel)
    logger.addHandler(console_handler)
    return logger
