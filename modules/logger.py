import logging
from datetime import datetime
import sys


def setup_logger(name, loglevel=logging.INFO):
	file_handler = logging.FileHandler(filename='logs/{}_{}.log'.format(name, datetime.now().strftime('%m_%d_%y')))
	stdout_handler = logging.StreamHandler(sys.stdout)
	handlers = [file_handler, stdout_handler]
	
	logging.basicConfig(
		level=loglevel, 
		format='[%(asctime)s] {%(filename)s:%(lineno)d} (%(funcName)s) %(levelname)s - %(message)s',
		handlers=handlers
	)

	logger = logging.getLogger(__name__)
	return logger
	
