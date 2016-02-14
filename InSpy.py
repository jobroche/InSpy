#!/usr/bin/env python2

# InSpy - A LinkedIn employee enumerator
# This script enumerates employees from any organization 
# using LinkedIn. Please note that this will not harvest all 
# employees within a given organization.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Author:  Jonathan Broche
# Contact: @g0jhonny
# Version: 1.0.1
# Date:    2015-11-22
#
# usage: ./inspy.py -c <company> [-d dept/title] [-e email output format] [-i input file with dept/titles] [-o output file]
# example: ./inspy.py -c abc -e flast@abc.com -o abc_employees.txt


import requests, BeautifulSoup, argparse, signal, time, datetime, os

start_time = time.time()

class colors:
    lightblue = "\033[1;36m"
    blue = "\033[1;34m"
    normal = "\033[0;00m"
    red = "\033[1;31m"
    yellow = "\033[1;33m"
    white = "\033[1;37m"
    green = "\033[1;32m"

#----------------------------------------#
#           HARVEST USERS                #
#----------------------------------------#

def inspy_enum(company, dept, ifile):
    try:
        dept_dictionary = ['sales', 'marketing', 'human resources', 'finance', 'accounting', 'inventory', 'quality assurance', 'insurance', 'licenses', 'operational', 'customer service', 'staff', 'research & development', 'management', 'administration', 'engineering', 'it', 'is', 'strategy', 'other']        
        
        employees = {}

        if dept is not None:
            dept_dictionary = [dept.lower()]

        if ifile is not None:
            try:
                if os.path.exists(ifile):            
                    with open(ifile, 'r') as f:
                        dept_dictionary = []
                        for line in f.readlines():
                            if line.rstrip():
                                dept_dictionary.append(line.rstrip())
            except IOError as e:
                print "{}[!]{} Problem opening the file. {}".format(e)

        for dd in dept_dictionary:
            print "{}[*]{} Searching for employees working at {} with '{}' in their title".format(colors.lightblue, colors.normal, company, dd)

            try:
                response = requests.get('https://www.linkedin.com/title/{}-at-{}'.format(dd.replace('-', ' '), company.replace('-', ' ')), timeout=2)
                if response.status_code == 200:
                    soup = BeautifulSoup.BeautifulSoup(response.text)
                else:
                    pass               
            except requests.exceptions.Timeout:
                print "{}[!]{} Timeout enumerating the {} department".format(colors.red, colors.normal, dd)
            except requests.exceptions.ConnectionError:
                print "{}[!]{} Connection error.".format(colors.red, colors.normal)
            except requests.exceptions.HTTPError:
                print "{}[!]{} HTTP error.".format(colors.red, colors.normal)

            #get employee names
            for n, t in zip(soup.findAll('h3', { "class" : "name" }), soup.findAll('p', { "class" : "headline" })):
                name = u''.join(n.getText()).encode('utf-8')
                title = u''.join(t.getText()).encode('utf-8').replace('&amp;', '&')

                if not name in employees:
                    employees[name] = title

        return employees
    except Exception as e:
        print "{}[!]{} Error harvesting users. {}".format(colors.red, colors.normal, e)

#----------------------------------------#
#               EMAILS                   #
#----------------------------------------#

def format_email(names, eformat):
    emails = []
    for name in names:
        spaces = []
        for x,y in enumerate(name):
            if ' ' in y:
                spaces.append(x)

        if eformat[:eformat.find('@')] == 'flast':
            emails.append('{}{}{}'.format(name[0], name[(spaces[-1]+1):], eformat[eformat.find('@'):]))
        elif eformat[:eformat.find('@')] == 'lfirst':
            emails.append('{}{}{}'.format(name[spaces[-1]+1], name[0:spaces[0]], eformat[eformat.find('@'):]))
        elif eformat[:eformat.find('@')] == 'first.last':
            emails.append('{}.{}{}'.format(name[0:spaces[0]],  name[(spaces[-1]+1):], eformat[eformat.find('@'):]))
        elif eformat[:eformat.find('@')] == 'last.first':
            emails.append('{}.{}{}'.format(name[(spaces[-1]+1):], name[0:spaces[0]], eformat[eformat.find('@'):]))

    return [e.lower() for e in emails]

#----------------------------------------#
#               OUTPUT                   #
#----------------------------------------#

def output(employees, email, company, ofile):
    counter = 0
    ge, be = {}, {}
    print '\n'

    if email:
        for k, e in zip(employees, email):
            if company in employees[k].lower():
                if ',' in k:
                     be[e] = '{}, {}'.format(k, employees[k])
                else:
                    ge[e] = '{}, {}'.format(k, employees[k])                    
                    print "{}[*]{} {}, {}, {}".format(colors.green, colors.normal, k.replace('&amp;', '&'), employees[k].replace('&amp;', '&'), e)
                    counter +=1
    else:
        for k in employees:
            if company in employees[k].lower():
                ge[k] = employees[k]
                print "{}[*]{} {} {}".format(colors.green, colors.normal, k.replace('&amp;', '&'), employees[k].replace('&amp;', '&'))
                counter +=1
    if be:        
        print "\n{}[!]{} The following employees have commas in their names. Their emails were not accurate.".format(colors.red, colors.normal)
        for k in be:           
            print "{}[*]{} {}".format(colors.yellow, colors.normal, be[k])

    if ofile:
        with open(ofile, 'w') as f:
            f.write("\n" + "-" * 69 + "\n" + "InSpy Output" + "\n" + "-" * 69 + "\n\n")
            
            if [e for e in ge.keys() if '@' in e]: #if emails in keys
                f.write("\n" + "E-mails" + "\n" + "-" * 25 + "\n\n")
                for k in ge.keys():
                    f.write(k+'\n')

                f.write("\n" + "All" + "\n" + "-" * 25 + "\n\n")
                for k in ge:
                    f.write('{}, {}\n'.format(ge[k], k))
            else:
               for k in ge:
                    f.write('{}, {}\n'.format(k, ge[k])) 

    print "\n{}[*]{} Done! {}{}{} employees found.".format(colors.lightblue, colors.normal, colors.green, counter,  colors.normal)
    print "{}[*]{} Completed in {:.1f}s\n".format(colors.lightblue, colors.normal, time.time()-start_time)

#----------------------------------------#
#               MAIN                     #
#----------------------------------------#

def main():
    print "\n " + "-" * 74 + "\n " + colors.white + "InSpy v1.0 - LinkedIn Employee Enumerator by Jonathan Broche (@g0jhonny)\n " + colors.normal + "-" * 74 + "\n "
    parser = argparse.ArgumentParser(description='InSpy - A LinkedIn employee enumerator by Jonathan Broche (@g0jhonny)')
    parser.add_argument('-c', '--company', required=True, help='Company name')
    parser.add_argument('-d', '--dept', nargs='?', const='', help='Department or title to query employees against. Inspy searches through a predefined list by default.')
    parser.add_argument('-e', '--emailformat', help='Email output format. Acceptable formats: first.last@xyz.com, last.first@xyz.com, flast@xyz.com, lastf@xyz.com')
    parser.add_argument('-i', '--inputfilename', nargs='?', const='', help='File with list of departments or titles to query employees against (one item per line)')
    parser.add_argument('-o', '--outfilename', nargs='?', const='', help='Output results to text file')
    args = parser.parse_args()

    employees = inspy_enum(args.company, args.dept, args.inputfilename)

    if args.emailformat:        
        if args.emailformat.find('@') and args.emailformat[:args.emailformat.find('@')] in {'flast', 'lfirst', 'first.last', 'last.first'}:
                if employees is not None:
                    e = format_email(employees.keys(), args.emailformat)
                    output(employees, e,args.company.lower(), args.outfilename)
        else:
            print "{}[!]{} Please provide a valid email address format (i.e., flast@xyz.com, lfirst@xyz.com, first.last@xyz.com, last.first@xyz.com)".format(colors.red, colors.normal)
    else:
        if employees is not None:
            output(employees,'',args.company.lower(), args.outfilename)

if __name__ == '__main__':
    main()