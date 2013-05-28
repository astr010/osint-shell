import requests
import urllib2
import urlparse
from bs4 import BeautifulSoup

from module import Module

class GoogleModule(Module):
    GOOGLE_SEARCH_URL = 'http://www.google.com/search'
    # http://clients1.google.com/complete/search?hl=en&output=toolbar&q=YOURSEARCHTERM
    # http://suggestqueries.google.com/complete/search?output=toolbar&hl=en&q=YOURSEARCHTERM
    GOOGLE_SUGGEST_URL = 'http://suggestqueries.google.com/complete/search' # output=toolbar&hl=en&q=YOURSEARCHTERM

    def __str__(self):
        return 'mod-google'

    def do_suggest(self, args):
        query = ' '.join(args)
        self.shell.print_line('suggest: %s' % query)
        html = requests.get(self.GOOGLE_SUGGEST_URL, params={
                            'q': query, 'output': 'toolbar', 'hl': 'fr'}).content
        soup = BeautifulSoup(html)
        for s in soup.find_all('suggestion'):
            self.shell.print_line(s.get('data', ''))

    def do_search(self, args):
        query = ' '.join(args)
        url_list = []
        self.shell.print_line('search: %s' % query)

        for i in (0, 10, 20):
            print 'Retreive results for page: %s' % i
            html = requests.get(self.GOOGLE_SEARCH_URL, params={
                       'q': query,'oq': query, 'hl': 'fr', 'start': i}).content
            soup = BeautifulSoup(html)
            for a in soup.find_all('a'):
                href = a.get('href', '/')
                url = urlparse.urljoin(self.GOOGLE_SEARCH_URL, href)
                parsed_url = urlparse.urlparse(url)
                parsed_query = urlparse.parse_qs(parsed_url.query)
                if parsed_url.path == '/url':
                    founded_url = parsed_query['q'][0]
                    parsed_url = urlparse.urlparse(founded_url)
                    if parsed_url.hostname != 'webcache.googleusercontent.com':
                        url_list.append(founded_url)

        for url in set(url_list):
            self.shell.print_line(url)

