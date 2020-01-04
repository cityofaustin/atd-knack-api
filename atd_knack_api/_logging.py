import logging
from logging.handlers import RotatingFileHandler

def get_logger(name):
    # init logger
    logger = logging.getLogger(name)

    # log rotate based on filesize
    file_handler = RotatingFileHandler(f"log/{name}.log", maxBytes=2000000)
    
    # print timestamp in logfile
    formatter = logging.Formatter(
        fmt="%(asctime)s %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    # send logs to console w/o timestamps
    console = logging.StreamHandler()

    logger.addHandler(console)

    return logger