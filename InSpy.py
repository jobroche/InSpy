#!/usr/bin/env python3
# Copyright (c) 2018 Jonathan Broche (@LeapSecurity)

import argparse, sys, os
from lib.workbench import *
from lib.soup import *
from lib.export import *
from lib.logger import *

hunterapi = "305d56f8420e160b5fb20dc09dc87c00fddbccc5"                                      #insert hunterio api key here

if not hunterapi:
	print("[+] Your hunter api key is Empty")
	print("[+] Hunter Api Key is required please fill the hunter api key opening the InSpy.py File")
	sys.exit(404)

Version ="4.0"

parser = argparse.ArgumentParser(description='InSpy - A LinkedIn enumeration tool by Hari Kiran(TheCyberMonster)\n A forked project of InSpy 3.0')
parser.add_argument('company', help="Company name to use for tasks.")
parser.add_argument('--domain', help="Company domain to use for searching.")
parser.add_argument('--email', help="Email format to create email addresses with. [Accepted Formats: first.last@xyz.com, last.first@xyz.com, firstl@xyz.com, lfirst@xyz.com, flast@xyz.com, lastf@xyz.com, first@xyz.com, last@xyz.com]")
parser.add_argument('--titles', metavar='file', default="wordlists/title-list-small.txt", nargs='?', help="Discover employees by title and/or department. Titles and departments are imported from a new line delimited file. [Default: title-list-small.txt]")
outgroup = parser.add_argument_group(title="Output Options")
outgroup.add_argument('--html', metavar='file', help="Print results in HTML file.")
outgroup.add_argument('--csv', metavar='file', help="Print results in CSV format.")
outgroup.add_argument('--json', metavar='file', help="Print results in JSON.")
outgroup.add_argument('--xml', metavar='file', help="Print results in XML.")

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()
start_logger(args.company)

email = args.email
domain = args.domain

print("\nInSpy {}".format(Version))

try:
	if domain and not email: #search hunter.io for email format
		email = get_email_format(args.domain, hunterapi)
	if email and not domain: #search clearbit for domain
		domain = get_domain(args.company)	
	if not email and not domain: #no domain or email provided - fully automate it
		domain = get_domain(args.company)
		if domain:
			email = get_email_format(domain, hunterapi)

	if email and domain:

		email = email.replace("{", "").replace("}","")

		print("Domain: {}, Email Format: {}".format(domain, email))

		employees = {}

		if os.path.exists(os.path.abspath(args.titles)):
			for response in search_linkedin(args.company, os.path.abspath(args.titles)):
				for name, title in get_employees(soupify(response)).items():
					if args.company.lower() in title.lower():
						if not name in employees:
							employees[name] = title
			print("{} Employees identified".format(len(employees.keys())))
		else:
			print(os.path.abspath(args.titles))
			print("No such file or directory: '{}'".format(args.titles))
		emails=[]
		if employees:
			#output employees
			for name, title in employees.items():
				print("{} {}".format(name, title[:50].replace('&amp;', '&')))
			
			#craft emails
			emails = create_emails(employees, domain, email)


			if emails:
				#output emails
				print("Emails crafted".format(len(emails.keys())))
				for name, email in emails.items():
					print(email)

		#export results
		if args.html:
			output("html", args.html, args.company, domain, employees, emails)
		if args.xml:
			output("xml", args.xml, args.company, domain, employees, emails)
		if args.json:
			output("json", args.json, args.company, domain, employees, emails)
		if args.csv:
			output("csv", args.csv, args.company, domain, employees, emails)
except (KeyboardInterrupt, SystemExit):
	print("Terminated script.")
