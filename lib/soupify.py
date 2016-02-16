from logger import *
import BeautifulSoup, json

def soupify(response):
    try:
        soupd = BeautifulSoup.BeautifulSoup(response)
        return soupd
    except (AttributeError, TypeError) as e:
        pass
    except Exception as e:
        perror("Error: {}".format(e))
        logging.error("Soupify.py Error: {}".format(e))

def get_employees(soup):
    try:
        employees = {}
        for n, t in zip(soup.findAll('h3', { "class" : "name" }), soup.findAll('p', { "class" : "headline" })):
            name = u''.join(n.getText()).encode('utf-8')
            title = u''.join(t.getText()).encode('utf-8')
            if name and title:
                employees[name] = title
        return employees
    except (AttributeError, TypeError) as e:
        pass
    except Exception as e:
        perror("Error: {}".format(e))
        logging.error("Soupify.py Error: {}".format(e))

def get_job_links(soup, company):
    try:
        job_links = []
        for link, comp in zip(soup.findAll('a', { "class" : "job-title-link" }), soup.findAll('span', { "class" : "company-name-text" })):
            if comp.text == company:
                job_links.append(u''.join(link['href']).encode('utf-8'))
        return job_links
    except (AttributeError, TypeError) as e:
        pass
    except Exception as e:
        perror("Error: {}".format(e))
        logging.error("Soupify.py Error: {}".format(e))

def get_page_links(soup):
    page_links = []
    try:
        for page in soup.findAll('li', { "class" : "page-number"}):
            a = page.findAll('a')
            page_links.append(u''.join("https://linkedin.com{}".format(a[0]['href'])).encode('utf-8'))
        return page_links
    except (AttributeError, TypeError) as e:
        pass
    except Exception as e:
        perror("Error: {}".format(e))
        logging.error("Soupify.py Error: {}".format(e))

def get_job_title(soup):
    try:
        return u''.join(json.loads(soup.find('code', {"id" : "decoratedJobPostingModule"}).string)['decoratedJobPosting']['jobPosting'].get('title')).encode('utf-8')
    except (AttributeError, TypeError) as e:
        pass
    except Exception as e:
        perror("Error: {}".format(e))
        logging.error("Soupify.py Error: {}".format(e))

def get_job_description(soup):
    try:
        return u''.join(json.loads(soup.find('code', {"id" : "decoratedJobPostingModule"}).string)['decoratedJobPosting']['jobPosting']['description'].get('rawText')).encode('utf-8')       
    except (AttributeError, TypeError):
        pass
    except Exception as e:
        perror("Error: {}".format(e))
        logging.error("Soupify.py Error: {}".format(e)) 