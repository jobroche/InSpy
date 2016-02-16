import logging, sys, time

time_format = time.strftime("%Y-%m-%d %H:%M:%S")

def start_logger(company):
	handler = logging.FileHandler('./logs/{}_{}.log'.format(company.replace(' ', '_'), time_format.replace(' ', '_')))
	handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s - %(message)s"))

	logger = logging.getLogger()
	logger.propagate = False
	logger.addHandler(handler)
	logger.setLevel(logging.INFO)
	logging.getLogger("requests").setLevel(logging.DEBUG)

class colors(object):
	grey = "\033[0;37m"
	cyan = "\033[0;36m"	
	yellow = "\033[0;33m"
	red = "\033[1;31m"
	normal = "\033[0;00m"

def pstatus(message):
	print "{} {}{}{}".format(time_format, colors.grey, message, colors.normal)

def presults(message):
	print "{} {}{}{}".format(time_format, colors.cyan, message, colors.normal)

def pwarning(message):
	print "{} {}{}{}".format(time_format, colors.yellow, message, colors.normal)

def perror(message):
	print "{} {}{}{}".format(time_format, colors.red, message, colors.normal)