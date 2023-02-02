import logging


# logging.basicConfig(format='%(asctime)s .... %(levelname)s: %(message)s', datefmt='%d/%m/%Y %H:%M:%S %p', level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s __%(levelname)s__ %(message)s', datefmt='%d/%m/%Y %H:%M:%S %p', level=logging.DEBUG)


# Comment out to show flask info messages in terminal
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)




