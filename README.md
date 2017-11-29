# InSpy

## Introduction
-----

InSpy is a python based LinkedIn enumeration tool. Inspy has two functionalities: TechSpy and EmpSpy.

- TechSpy - Crawls LinkedIn job listings for technologies used by the provided company. InSpy attempts to identify technologies by matching job descriptions to keywords from a new line delimited file.

- EmpSpy - Crawls LinkedIn for employees working at the provided company. InSpy searches for employees by title and/or departments from a new line delimited file. InSpy may also create emails for the identified employees if the user specifies an email format.

## Installation
-----

Run `pip install -r requirements.txt` within the cloned InSpy directory.

## Help
-----

```
InSpy - A LinkedIn enumeration tool by Jonathan Broche (@jonathanbroche)

positional arguments:
  company               Company name to use for tasks.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit

Technology Search:
  --techspy [file]      Crawl LinkedIn job listings for technologies used by
                        the company. Technologies imported from a new line
                        delimited file. [Default: tech-list-small.txt]
  --limit int           Limit the number of job listings to crawl. [Default:
                        50]

Employee Harvesting:
  --empspy [file]       Discover employees by title and/or department. Titles
                        and departments are imported from a new line delimited
                        file. [Default: title-list-small.txt]
  --emailformat string  Create email addresses for discovered employees using
                        a known format. [Accepted Formats: first.last@xyz.com,
                        last.first@xyz.com, first_last@xyz.com, last_first@xyz.com, 
                        firstl@xyz.com, lfirst@xyz.com,
                        flast@xyz.com, lastf@xyz.com, first@xyz.com,
                        last@xyz.com]

Output Options:
  --html file           Print results in HTML file.
  --csv file            Print results in CSV format.
  --json file           Print results in JSON.
```
