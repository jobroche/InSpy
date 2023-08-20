
from html.parser import HTMLParser
import logging
from lib.http import http_request

def get_domain(company):                #Clearbit API - clearbit.com

	clearbit_request = "https://autocomplete.clearbit.com/v1/companies/suggest?query={}".format(company)
	clearbit_results = []
	domain = ""

	r = http_request(clearbit_request)
	if len(r["response"]) >=1:
		if len(r["response"]) >= 1:
			for element in r["response"]:
				clearbit_results.append({"name": element['name'], "domain": element['domain']})

		if len(clearbit_results) == 1:                            #return domain if one result
			domain = clearbit_results[0]["domain"]
		elif len(clearbit_results) > 1:                           #prompt user if multiple domains identified
			print("Multiple domains identified for company. Which one is the target?")
			for index, result in enumerate(clearbit_results):
				print("{}) Name: {}, Domain: {}".format(index, result["name"], result["domain"]))
			choice = int(input("Select using S.No \n (Ex: select-> 1 )\n select-> "))
			domain = clearbit_results[choice]["domain"]

	if domain:
		return domain
	else:
		logging.error("Clearbit API - HTTP {} Error".format(r["status"]))
		print("InSpy could not identify the domain name. Use --domain.")


def get_email_format(domain, apikey): #HunterIO API - hunter.io
	hunter_request = "https://api.hunter.io/v2/domain-search?domain={domain}&api_key={api}".format(domain=domain, api=apikey)
	emailformat = ""

	r = http_request(hunter_request)

	if r["status"] == 200:
		for k,v in r["response"].items():
			if k == 'data':
				if v['pattern']:
					emailformat = v['pattern']
					logging.info("HunterIO Returned Email Format: {}".format(emailformat))
	else:
		logging.error("HunterIO - HTTP {} Error".format(r["status"]))

	if emailformat:
		return emailformat
	else:
		print("InSpy could not identify the email format. Use --email.")

def search_linkedin(company, file):
	titles = []
	responses = []

	with open(file) as f:
		for title in f.readlines():
			titles.append(title.rstrip())
	
	for title in titles:
		response = http_request("https://www.linkedin.com/title/{}-at-{}".format(title.replace(' ', '-'), company.replace(' ', '-')))
		if response["status"] == 200:
			responses.append(response["response"])
		elif response["status"] == 999: #LinkedIn doesn't like InSpy
			logging.error("LinkedIn Search - HTTP 999 Error Crawling {}".format(title))
			pass
		else:
			logging.error("LinkedIn Search - HTTP {} Error Crawling {}".format(response["status"], title))
			pass
	return responses


#craft emails

def create_emails(employees, domain, eformat):
	hparser=HTMLParser.HTMLParser()
	emails = {}

	for name in employees.keys(): #split up employee name by first, last name
		try:
			first = hparser.unescape([n.split() for n in name.split(',',1)][0][0])
			last = hparser.unescape([n.split() for n in name.split(',',1)][0][-1])
		except UnicodeDecodeError:
			first = [n.split() for n in name.split(',',1)][0][0]
			last = [n.split() for n in name.split(',',1)][0][-1]
		
		#create emails
		email = "{}@{}".format(format_email(eformat.split("@")[0], first.lower(), last.lower()), domain)

		if email:
			emails[name] = email

	if emails:
		return emails
		
def format_email(eformat, first, last):
	try:
		formats = {
			'first.last': '{}.{}'.format(first,last),
			'last.first': '{}.{}'.format(last,first),
			'firstlast': '{}{}'.format(first,last),
			'lastfirst': '{}{}'.format(last,first),
			'first_last': '{}_{}'.format(first,last),
			'last_first': '{}_{}'.format(last,first),
			'firstl':'{}{}'.format(first,last[0]),
			'lfirst':'{}{}'.format(last[0],first), 
			'flast': '{}{}'.format(first[0],last),
			'lastf': '{}{}'.format(last,first[0]),
			'first': first,
			'last': last
		}
		return formats[eformat]
	except Exception as e:
		print(e)
