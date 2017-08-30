from logger import *
import requests
requests.packages.urllib3.disable_warnings()

headers={'Host':'www.linkedin.com', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}


def crawl_employees(company, file):
	titles = []
	responses = []
	try:
		with open(file) as f:
			for title in f.readlines():
				titles.append(title.rstrip())
		for title in titles:
			response = requests.get("https://www.linkedin.com/title/{}-at-{}".format(title.replace(' ', '-'), company.replace(' ', '-')), timeout=3, headers=headers)
			responses.append(response.text)
	except requests.exceptions.Timeout as e:
		pwarning("Warning: Timed out crawling {}".format(title))
	except Exception as e:
		perror("Error: {}".format(e))
		logging.error(e)
	return responses

def crawl_jobs(company): #initial crawl
	url = "https://www.linkedin.com/jobs/{}-jobs".format(company.replace(' ', '-'))
	try:
		response = requests.get(url, timeout=3, headers=headers)
		return response.text
	except requests.exceptions.Timeout as e:
		perror("Error: Timed out. Try again, LinkedIn doesn't like us sometimes")
		logging.error(e)
	except requests.exceptions.ReadTimeout as e:
		perror("Error: Read time out")
		logging.error(e)
	except Exception as e:
		perror("Error: {}".format(e))
		logging.error(e)


def crawl_url(url=None): #page crawls
	try:
		response = requests.get(url, timeout=3, headers=headers)
		return response.text
	except requests.exceptions.Timeout as e:
		pwarning("Warning: Timed out")
	except requests.exceptions.ReadTimeout as e:
		pwarning("Warning: Read time out")
	except Exception as e:
		pwarning("Warning: {}".format(e))
		logging.error(e)