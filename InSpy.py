#!/usr/bin/env python2

from lib.logger import *
from lib.soupify import *
from lib.workbench import *
from lib.crawler import *
import os, argparse, sys, time

parser = argparse.ArgumentParser(description='InSpy - A LinkedIn enumeration tool by Jonathan Broche (@g0jhonny)', version="2.0")
parser.add_argument('company', help="Company name to use for tasks.")    
techgroup = parser.add_argument_group(title="Technology Search")
techgroup.add_argument('--techspy', metavar='file', const="wordlists/tech-list-small.txt", nargs='?', help="Crawl LinkedIn job listings for technologies used by the company. Technologies imported from a new line delimited file. [Default: tech-list-small.txt]")
techgroup.add_argument('--limit', metavar='int', type=int, default=50, help="Limit the number of job listings to crawl. [Default: 50]")
empgroup = parser.add_argument_group(title="Employee Harvesting")
empgroup.add_argument('--empspy', metavar='file', const="wordlists/title-list-small.txt", nargs='?', help="Discover employees by title and/or department. Titles and departments are imported from a new line delimited file. [Default: title-list-small.txt]")
empgroup.add_argument('--emailformat', metavar='string', help="Create email addresses for discovered employees using a known format. [Accepted Formats: first.last@xyz.com, last.first@xyz.com, firstl@xyz.com, lfirst@xyz.com, flast@xyz.com, lastf@xyz.com, first@xyz.com, last@xyz.com]")
outgroup = parser.add_argument_group(title="Output Options")
outgroup.add_argument('--html', metavar='file', help="Print results in HTML file.")
outgroup.add_argument('--csv', metavar='file', help="Print results in CSV format.")
outgroup.add_argument('--json', metavar='file', help="Print results in JSON.")

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()
start_logger(args.company)

print "\nInSpy {}\n".format(parser.version)

if not args.techspy and not args.empspy: 
    print "You didn't provide any work for me to do."
    sys.exit(1)

stime = time.time()
tech_html, employee_html, tech_csv, employee_csv, employee_json = [], [], [], [], []

if args.techspy:
    if os.path.exists(os.path.abspath(args.techspy)):
        initial_crawl = crawl_jobs(args.company)
        if initial_crawl:
            soup = soupify(initial_crawl)
            job_links = []
            for link in get_job_links(soup, args.company):
                if len(job_links) < args.limit:
                    job_links.append(link)
            if len(job_links) != args.limit:
                page_links = get_page_links(soup)
                for page in range(len(page_links)):
                    if len(job_links) == args.limit: break
                    urlcrawl = crawl_url(page_links[page])
                    if urlcrawl:                    
                        for link in get_job_links(soupify(urlcrawl), args.company):
                            if len(job_links) < args.limit:
                                job_links.append(link)

            pstatus("{} Jobs identified".format(len(job_links)))
            if job_links:
                techs = {}            
                for job in range(len(job_links)):
                    jobresponse = crawl_url(job_links[job])
                    if jobresponse:
                        jobsoup = soupify(jobresponse)
                        description = get_job_description(jobsoup)
                        matches = identify_tech(description, os.path.abspath(args.techspy))
                        if matches:
                            title = get_job_title(jobsoup)
                            techs[title] = {job_links[job]:matches}

                tech_html, tech_csv, tech_json = craft_tech(techs)
    else:
        perror("No such file or directory: '{}'".format(args.techspy))

if args.empspy:
    if os.path.exists(os.path.abspath(args.empspy)):
        employees = {}
        emails = []
        for response in crawl_employees(args.company, os.path.abspath(args.empspy)):
            for name, title in get_employees(soupify(response)).items():
                if args.company.lower() in title.lower():
                    if not name in employees:
                        employees[name] = title

        pstatus("{} Employees identified".format(len(employees.keys())))
        if employees:
            if args.emailformat:
                if args.emailformat[:args.emailformat.find('@')] in ['first.last', 'last.first', 'firstlast', 'lastfirst', 'first', 'last', 'firstl', 'lfirst', 'flast', 'lastf']:
                    employee_html, employee_csv, employee_json = craft_employees(employees, args.emailformat)
                else:
                    pwarning("You didn't provide a valid e-mail format. See help (-h) for acceptable formats.")
                    employee_html, employee_csv, employee_json = craft_employees(employees, None)
            else:
                employee_html, employee_csv, employee_json = craft_employees(employees, None)
    else:
        print os.path.abspath(args.empspy)
        perror("No such file or directory: '{}'".format(args.empspy))

#output
if args.html:
    if tech_html or employee_html:
        if tech_html and employee_html:
            craft_html(args.company, tech_html, employee_html, args.html)
        elif tech_html and not employee_html:
            craft_html(args.company, tech_html, None, args.html)
        else:
            craft_html(args.company, None, employee_html, args.html)
if args.csv:
    if tech_csv or employee_csv:
        if tech_csv and employee_csv:
            craft_csv(tech_csv, employee_csv, args.csv)
        elif tech_csv and not employee_csv:
            craft_csv(tech_csv, None, args.csv)
        else:
            craft_csv(None, employee_csv, args.csv)
if args.json:
    if tech_json or employee_json:
        if tech_json and employee_json:
            craft_json(tech_json, employee_json, args.json)
        elif tech_json and not employee_json:
            craft_json(tech_json, None, args.json)
        else:
            craft_json(None, employee_json, args.json)

print "Completed in {:.1f}s".format(time.time()-stime)