import re
from bs4 import BeautifulSoup
import requests

def download_wikipedia_site(url):

    r = requests.get(url)
    return r.text

def get_rows(html):

    soup = BeautifulSoup(html)
    tables = soup.findAll('table', {'class':'wikitable'})

    rows = []
    for table in tables:
        rs = BeautifulSoup('%s'%table).findAll('tr')
        state = ''
        for r in rs:
            th = BeautifulSoup('%s'%r).findAll('th')
            if len(th) != 0:
                state = BeautifulSoup('%s'%th).findAll('span')[0].get('id')
            else:
                #print r
                td = BeautifulSoup('%s'%r).findAll('td')
                try:
                    town = BeautifulSoup('%s'%td[0]).findAll('a')[0].getText()
                except:
                    town = BeautifulSoup('%s'%td[0]).getText()
                try:
                    wiki_link = 'http://en.wikipedia.org{0}'.format(BeautifulSoup('%s'%td[1]).findAll('a')[0].get('href'))
                except:
                    wiki_link = None
                try:
                    station = BeautifulSoup('%s'%td[1]).findAll('a')[0].getText()
                except:
                    station = None
                freq = BeautifulSoup('%s'%td[2]).getText()
                rows.append({
                    'state': state,
                    'town': town,
                    'wiki_link': wiki_link,
                    'station': station,
                    'freq': freq,
                })
                #print rows
                #raise Exception('debug')

    return rows

def get_station_website(wiki_link):

    if wiki_link == None:
        return None

    pattern = re.compile(r'Website')

    html = requests.get(wiki_link).text
    th = BeautifulSoup(html).find('th', text=pattern)

    if th == None:
        return None

    #print th
    #print th.parent
    #print th.parent.findAll('td')[0]
    #raise Exception('debug')

    station_url = th.parent.findAll('td')[0].findAll('a')[0].get('href')

    return station_url

if __name__ == '__main__':

    url = "http://en.wikipedia.org/wiki/List_of_NPR_stations"

    html = download_wikipedia_site(url)
    rows = get_rows(html)
    for i in range(0, len(rows)):
        rows[i]['station_url'] = get_station_website(rows[i]['wiki_link'])
        #print rows[i]
        #raise Exception('debug')

        print "{0}/{1}".format(i, len(rows))

    print rows
        

