
import logging,time

time_format = time.strftime("%Y-%m-%d %H:%M:%S")

def start_logger(company):
	handler = logging.FileHandler('./logs/{}_{}.log'.format(company.replace(' ', '_'), time_format.replace(' ', '_')))
	handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s - %(message)s"))

	logger = logging.getLogger()
	logger.propagate = False
	logger.addHandler(handler)
	logger.setLevel(logging.INFO)
	logging.getLogger("requests").setLevel(logging.DEBUG)