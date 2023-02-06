import logging

class ColoredFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno == logging.WARNING:
            color = '\033[33m'  # yellow
        elif record.levelno == logging.ERROR:
            color = '\033[31m'  # red
        elif record.levelno == logging.INFO:
            color = '\033[32m'  # green
        elif record.levelno == logging.DEBUG:
            color = '\033[34m'  # blue
        else:
            color = '\033[0m'  # default color
        reset = '\033[0m'
        record.levelname = f'{color}{record.levelname}{reset}'
        record.msg = f'{color}{record.msg}{reset}'
        return super().format(record)

formatter = ColoredFormatter(fmt='%(asctime)s %(levelname)s: %(message)s', datefmt='%d/%m/%Y %H:%M:%S %p')

logger = logging.getLogger()
# set the logging level to DEBUG
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)


# Comment out to show flask info messages in terminal
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)

