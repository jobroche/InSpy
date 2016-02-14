# InSpy

A python based LinkedIn employee enumerator. This script is great for social engineering assessments where clients ask one
to provide employee emails.

### Help

```
InSpy - A LinkedIn employee enumerator by Jonathan Broche (@g0jhonny)

optional arguments:
  -h, --help            show this help message and exit
  -c COMPANY, --company COMPANY
                        Company name
  -d [DEPT], --dept [DEPT]
                        Department or title to query employees against. Inspy
                        searches through a predefined list by default.
  -e EMAILFORMAT, --emailformat EMAILFORMAT
                        Email output format. Acceptable formats:
                        first.last@xyz.com, last.first@xyz.com, flast@xyz.com,
                        lastf@xyz.com
  -i [INPUTFILENAME], --inputfilename [INPUTFILENAME]
                        File with list of departments or titles to query
                        employees against (one item per line)
  -o [OUTFILENAME], --outfilename [OUTFILENAME]
                        Output results to text file
```
### Examples

```
./InSpy.py -c "acme corp"

 --------------------------------------------------------------------------
 InSpy v1.0 - LinkedIn User Enumerator by Jonathan Broche (@g0jhonny)
 --------------------------------------------------------------------------
 
[*] Searching for employees working at acme corp with 'sales' in their title
[*] Searching for employees working at acme corp with 'hr' in their title
[*] Searching for employees working at acme corp with 'marketing' in their title
[*] Searching for employees working at acme corp with 'finance' in their title
[*] Searching for employees working at acme corp with 'accounting' in their title
[*] Searching for employees working at acme corp with 'director' in their title
[*] Searching for employees working at acme corp with 'administrative' in their title
[*] Searching for employees working at acme corp with 'lawyer' in their title
[*] Searching for employees working at acme corp with 'it' in their title
[*] Searching for employees working at acme corp with 'security' in their title


[*] Proud Arkie Accounts Receivable specialist at Acme Corp.
[*] Brian Russo Finance Manager at Acme corp
[*] Paul Samuelson Director of Customer Support at ACME Corp. Production Resources
[*] Steve Smith Developer at Acme Corp
[*] Sarah Rhodes Director of Sales at Acme Corp
[*] Frances Jones Assistant to the Director at Acme Corp
 ...snip...

[*] Done! 29 employees found.
[*] Completed in 28.7s
```

Provide InSpy with the email format of the respective corporation and it'll output the emails for you.

```
./InSpy.py -c 'acme corp' -e flast@acme.com

 --------------------------------------------------------------------------
 InSpy v1.0 - LinkedIn User Enumerator by Jonathan Broche (@g0jhonny)
 --------------------------------------------------------------------------
 
[*] Searching for employees working at acme corp with 'sales' in their title
[*] Searching for employees working at acme corp with 'hr' in their title
[*] Searching for employees working at acme corp with 'marketing' in their title
[*] Searching for employees working at acme corp with 'finance' in their title
[*] Searching for employees working at acme corp with 'accounting' in their title
[*] Searching for employees working at acme corp with 'director' in their title
[*] Searching for employees working at acme corp with 'administrative' in their title
[*] Searching for employees working at acme corp with 'lawyer' in their title
[*] Searching for employees working at acme corp with 'it' in their title
[*] Searching for employees working at acme corp with 'security' in their title


[*] Proud Arkie, Accounts Receivable specialist at Acme Corp., parkie@acme.com
[*] Brian Russo, Finance Manager at Acme corp, brusso@acme.com
[*] Paul Samuelson, Director of Customer Support at ACME Corp. Production Resources, psamuelson@acme.com
[*] Steve Smith, Developer at Acme Corp, ssmith@acme.com
[*] Sarah Rhodes, Director of Sales at Acme Corp, srhodes@acme.com
[*] Frances Jones, Assistant to the Director at Acme Corp, fjones@acme.com
 ...snip...

[*] Done! 29 employees found.
[*] Completed in 29.0s

```