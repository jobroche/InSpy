
import requests, random
import logging

def random_header():

	agents = ['Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3']

	return {'User-Agent': random.choice(agents),'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}

def http_request(url):

	try:
		r = requests.get(url, timeout=3, headers=random_header())

		if r.status_code == 200:
			if "linkedin.com" in url:
				return {"status": r.status_code, "response": r.text}
			else:
				return {"status": r.status_code, "response": r.json()}
		else: 
			return {"status": r.status_code, "response": ""}

	except requests.exceptions.Timeout as e:
		print("Error: Timed out.")
		logging.error(e)
	except Exception as e:
		logging.error(e)
