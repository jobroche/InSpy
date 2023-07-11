# InSpy

⛔ [DEPRECATED]. This repo is no longer being maintained.

## Introduction
-----

InSpy is a python based LinkedIn enumeration tool.

Version 3.0 introduces the automation of domain and email retrieval in addition to randomized headers and xml output support.

## Installation
-----

Run `pip install -r requirements.txt` within the cloned InSpy directory.

Obtain an API key from [HunterIO](https://hunter.io/) and insert it into the hunterio variable within InSpy.py (line 29).

## Help
-----

```
InSpy - A LinkedIn enumeration tool by Jonathan Broche (@LeapSecurity)

positional arguments:
  company          Company name to use for tasks.

optional arguments:
  -h, --help       show this help message and exit
  -v, --version    show program's version number and exit
  --domain DOMAIN  Company domain to use for searching.
  --email EMAIL    Email format to create email addresses with. [Accepted
                   Formats: first.last@xyz.com, last.first@xyz.com,
                   firstl@xyz.com, lfirst@xyz.com, flast@xyz.com,
                   lastf@xyz.com, first@xyz.com, last@xyz.com]
  --titles [file]  Discover employees by title and/or department. Titles and
                   departments are imported from a new line delimited file.
                   [Default: title-list-small.txt]

Output Options:
  --html file      Print results in HTML file.
  --csv file       Print results in CSV format.
  --json file      Print results in JSON.
  --xml file       Print results in XML.
```
