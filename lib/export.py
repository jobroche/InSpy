import json, os, xml.dom.minidom, time
from xml.etree.ElementTree import Element, SubElement, tostring

def output(format, file, company, domain, employees, emails):
	if format == "xml":
		oxml(file, company, domain, employees, emails)
	if format == "csv":
		ocsv(file, company, domain, employees, emails)
	if format == "html":
		ohtml(file, company, domain, employees, emails)
	if format == "json":
		ojson(file, company, domain, employees, emails)

#CSV
def ocsv(filename, company, domain, employees, emails):
	with open(os.path.abspath(filename), 'a') as csvfile:
		fieldnames = ["Employee Name", "Title", "Email"]
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		for name, title in employees.iteritems():
			writer.writerow({"Employee Name": name, "Title": title.replace('&amp;', '&'), "Email": emails[name]})

#JSON
def ojson(file, company, domain, employees, emails):
	employee_json = []

	for name, title in employees.iteritems():
		employee_json.append({"name": name, "title": title.replace('&amp;', '&'), "email": emails[name]})

	full_json = {
	"company": {"name":company, "domain": domain},
	"employees": employee_json
	}

	with open(os.path.abspath(file), 'w') as f:
		f.write(json.dumps(full_json))

#XML
def oxml(file, company, domain, employees, emails):
	top = Element('InSpy')
	cxml = SubElement(top, 'Company')

	#company name
	cnxml = SubElement(cxml, "Name")
	cnxml.text = company
	#company domain
	cdxml = SubElement(cxml, "Domain")
	cdxml.text = domain

	echild = SubElement(top, 'Employees')

	for name, title in employees.iteritems():
		
		employee = SubElement(echild, "Employee")		
		#name
		nxml = SubElement(employee, "Name")
		nxml.text = name
		#title
		txml = SubElement(employee, "Title")
		txml.text = title.replace("&amp;", "&")
		#email
		exml = SubElement(employee, "Email")
		exml.text = emails[name]

	fxml = xml.dom.minidom.parseString(tostring(top))

	with open(os.path.abspath(file), 'w') as f:
		f.write(fxml.toprettyxml())

#HTML
def ohtml(file, company, domain, employees, emails):
	employee_html = []

	for name, title in employees.iteritems():
		employee_html.append("<tr><td>{name}</td><td>{title}</td><td>{email}</td></tr>".format(name=name, title=title, email=emails[name]))

	page = """
	<html>
	<head><title>InSpy - {company}</title>
	<meta charset="UTF-8">
	</head>
	<body style='font-family: arial, sans-serif; font-size: 14px; margin: 10px 0 0 20px;'>
	<h2>InSpy</h2>
	<p>Company: {company}</p><p>Date: {time}</p>
	<table border='1'>
		<tr style='background-color: #0057b8; color: #fff;'>
			<th>Employee Name</th>
			<th>Title</th>
			<th>E-mail</th>
		</tr>
		{html}
	</table>
	<br/>
	</body>
	</html>
	""".format(company=company, time=time.strftime("%Y/%m/%d %H:%M:%S"), html=employee_html)

	with open(os.path.abspath(file), 'w') as f:
		f.write(page)