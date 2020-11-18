
from bs4 import BeautifulSoup

def soupify(response):
    try:
        soupd = BeautifulSoup.BeautifulSoup(response)
        return soupd
    except (AttributeError, TypeError) as e:
        pass
    except Exception as e:
        print("Error: {}".format(e))

def get_employees(soup):
    try:
        employees = {}
        for n, t in zip(soup.findAll('a', {"class": "professional__name"}), soup.findAll("p", {"class" : "professional__headline"})):
            name = n.getText().encode('ascii','ignore')
            title = t.getText().encode('ascii','ignore')
            if name and title:
                employees[name] = title
        return employees
    except (AttributeError, TypeError) as e:
        pass
    except Exception as e:
        print("Error: {}".format(e))

