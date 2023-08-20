
import requests, random
import logging

def random_header():
	agents = ['Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/25.0',
			  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
			  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
			  'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41',
			  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36']

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
