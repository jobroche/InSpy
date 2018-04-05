import re, json, os, csv, time, codecs, HTMLParser
from logger import *

def identify_tech(data, file):
	matches = []
	with open(file) as f:
		keywords = f.readlines()

	for sentence in data.lower().split("."):
		keyword_found = []
		for keyword in keywords:
			if re.findall('\\b{}\\b'.format(re.escape(keyword.rstrip())), re.escape(sentence)):
				keyword_found.append(keyword.rstrip())
		if keyword_found:
			matches.append({sentence:keyword_found})
	return matches

def craft_tech(matches):
	logging.info(matches)
	unique_techs, html_out, csv_out, json_out = [], [], [], []
	for title, link in matches.items():
		techs_per_job = []
		for url in link.keys():
			for data in link.get(url):
				for sentence, techs in data.items():
					highlight_techs = sentence
					for tech in techs:
						if tech not in unique_techs: unique_techs.append(tech)
						if tech not in techs_per_job: techs_per_job.append(tech)
						highlight_techs = re.sub('\\b{}\\b'.format(tech), '<span style="background-color: #FFFF00">{}</span>'.format(tech), highlight_techs)
					html_out.append("<tr><td style='width:30%; padding: 5px;'><a href='{url}' target='_blank'>{title}</a></td><td style='width:15%; padding: 5px; text-align:center;'>{techs}</td><td style='width:55%; padding: 5px;'>{sentence}</td></tr>".format(title=title,techs=', '.join(techs),sentence=highlight_techs.replace("\xe2\x80\xa2", " * "),url=url))
					csv_out.append({"Job Title": title, "Technologies": ', '.join(techs), "Excerpt": sentence, "URL": url})
					json_out.append({"jobtitle": title, "technologies": ', '.join(techs), "excerpt": sentence, "url": url})

		pstatus('Title: {}'.format(title))
		presults(', '.join(techs_per_job))

	if unique_techs:
		pstatus("Unique Technologies:")
		presults(', '.join(unique_techs))

	return html_out, csv_out, json_out

def craft_employees(employees, eformat):
	hparser=HTMLParser.HTMLParser()
	html_out, csv_out, json_out = [], [], []
	emails = {}
	if eformat:
		format = eformat[:eformat.find('@')]
		domain = eformat[eformat.find('@'):]

		for name in employees.keys():
			try:
				first = hparser.unescape([n.split() for n in name.split(',',1)][0][0])
				last = hparser.unescape([n.split() for n in name.split(',',1)][0][-1])
			except UnicodeDecodeError:
				first = [n.split() for n in name.split(',',1)][0][0]
				last = [n.split() for n in name.split(',',1)][0][-1]
			email = "{}{}".format(format_email(format, first.lower(), last.lower()), domain)
			if email:
				emails[name] = email

	for name, title in employees.items():
		try:
			name = hparser.unescape(name)
			title = hparser.unescape(title)
		except UnicodeDecodeError:
			pass
		presults("{} {}".format(name, title[:50].replace('&amp;', '&')))
		logging.info("Employees identified: {}".format(employees))

		#html output
		if emails:
			html_out.append("<tr><td>{name}</td><td>{title}</td><td>{email}</td></tr>".format(name=name, title=title, email=emails.get(name)))
			csv_out.append({"Employee Name": name, "Title": title, "Email": emails.get(name)})
			json_out.append({"employeename": name, "title": title, "email": emails.get(name)})
		else:
			html_out.append("<tr><td>{name}</td><td>{title}</td><td>--</td></tr>".format(name=name, title=title))
			csv_out.append({"Employee Name": name, "Title": title, "Email": "--"})
			json_out.append({"employeename": name, "title": title, "email": "--"})

	if emails:
		pstatus("Emails crafted")
		for name, email in emails.items():
			presults(email)


	
	return html_out, csv_out, json_out

def format_email(format, first, last):
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
		return formats[format]
	except Exception as e:
		logging.error(e)


def craft_html(company, tech_html, employee_html, filename):
	if tech_html:
		tech_table = """
		<h4>Technologies Identified</h4>
		<table border='1'>
			<tr style='background-color: #0057b8; color: #fff;'>
				<th>Job Title</th>
				<th>Technologies</th>
				<th>Excerpt</th>
			</tr>
			<!--results-->
			{techs}	
		</table>
		""".format(techs=' '.join(tech_html))
	else: tech_table = ""

	if employee_html:
		employee_table = """
		<h4>Employees Identified</h4>
		<table border='1'>
			<tr style='background-color: #0057b8; color: #fff;'>
				<th>Employee Name</th>
				<th>Title</th>
				<th>E-mail</th>
			</tr>
			{html}
		</table>
		""".format(html=' '.join(employee_html))
	else: employee_table = ""

	page = """
	<html>
	<head><title>InSpy - {company}</title>
	<meta charset="UTF-8">
	</head>
	<body style='font-family: arial, sans-serif; font-size: 14px; margin: 10px 0 0 20px;'>
	<h2>InSpy</h2>
	<p>Company: {company}</p><p>Date: {time}</p>
	{tech}
	{emp}
	<br/>
	</body>
	</html>
	""".format(company=company, time=time.strftime("%Y/%m/%d %H:%M:%S"), tech=tech_table, emp=employee_table)

	with open(os.path.abspath(filename), 'w') as f:
		f.write(page)

def craft_csv(tech_csv, employee_csv, filename):

	if tech_csv:
		with open(os.path.abspath(filename), 'w') as csvfile:
			fieldnames = ["Job Title", "Technologies", "Excerpt", "URL"]
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)	
			writer.writeheader()
			for row in tech_csv:
				writer.writerow(row)
			writer.writerow({})

	if employee_csv:
		with open(os.path.abspath(filename), 'a') as csvfile:
			fieldnames = ["Employee Name", "Title", "Email"]
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			writer.writeheader()
			for row in employee_csv:
				writer.writerow(row)

def craft_json(tech_json, employee_json, filename):
	if tech_json and employee_json:
		tech = {"technologies":tech_json}
		emp = {"employees":employee_json}
		full_json = tech.copy()
		full_json.update(emp)
	elif tech_json:
		tech = {"technologies":tech_json}
		full_json = tech
	elif employee_json:
		emp = {"employees":employee_json}
		full_json = emp

	with open(os.path.abspath(filename), 'w') as f:
		f.write(json.dumps(full_json))
