import re
import lxml
from lxml import etree
import json
import string
import requests
import urllib2
import urlparse
from bs4 import BeautifulSoup

from module import Module

class HTTPResponse(object):
    XPATH_QUERY_ENCODING = "/html/head/meta[@http-equiv='Content-Type']/@content|/html/head/meta[@http-equiv='Content-type']/@content|/html/head/meta[@http-equiv='content-type']/@content"
    DEFAULT_RESPONSE_ENCODAGE = 'UTF-8'

    XPATH_QUERY_PAGE_TITLE = "//title/text()"
    XPATH_QUERY_RSS_FEEDS = "//link[@type='application/rss+xml']/@href"
    XPATH_QUERY_TITLES = "//h{i}/*/text()|//h{i}/text()"
    XPATH_QUERY_ANCHORS = "//a/@href"

    def __init__(self, url):
        self.raw_resp = urllib2.urlopen(url)
        self.code = self.raw_resp.getcode()
        self.url = self.raw_resp.geturl()
        self.body = self.raw_resp.read()
        self.headers = self.raw_resp.info()
        self.soup = BeautifulSoup(self.body)
        self.parsed_data = etree.fromstring(self.body,
                                    etree.HTMLParser(encoding=self.encoding))

    @property
    def anchors(self):
        anchors = [urlparse.urljoin(self.url, href)
                        for href in self.parsed_data.xpath(
                                self.XPATH_QUERY_ANCHORS)]
        return sorted(set(anchors))

    @property
    def page_title(self):
        return self.parsed_data.xpath(self.XPATH_QUERY_PAGE_TITLE)[0]

    @property
    def rss_feeds(self):
        return self.parsed_data.xpath(self.XPATH_QUERY_RSS_FEEDS)

    @property
    def encoding(self):
        try:
            for header in self.headers:
                if header.lower() == 'content-type':
                    return re.search(r"charset=(.*)",
                                self.headers[header]).group(1)
        except:
            # print "Cannot detect encoding in HTTP Headers. Test in HTML document."
            pass

        try:
            parsed_data = etree.fromstring(self.body, etree.HTMLParser())
            return re.search(r"charset=(.*)", parsed_data.xpath(
                        self.XPATH_QUERY_ENCODING)[0]).group(1)
        except:
            # print "Cannot detect encoding in HTML document."
            # print "Fixed at '%s'." % self.DEFAULT_RESPONSE_ENCODAGE
            pass
        return self.DEFAULT_RESPONSE_ENCODAGE

    @property
    def titles(self):
        titles = []
        for i in range(0, 6):
            for txt in self.parsed_data.xpath(self.XPATH_QUERY_TITLES.format(i=i)):
                titles.append({'tag': 'H{i}'.format(i=i),
                               'content': txt.strip()})
        return titles

    def xpath_query(self, query):
        return self.parsed_data.xpath(query)

    def css_select(self, query):
        return self.soup.select(query)

    def __str__(self):
        return urlparse.urlparse(self.url).hostname


class HTTPModule(Module):

    def do_request_get(self, args):
        self.current_response = HTTPResponse(' '.join(args))
        self.shell.print_line(self.current_response.code)

    def do_response_headers(self, args):
        for header in self.current_response.headers:
            self.shell.print_line(
                    '{k}: {v}'.format(k=string.ljust(header, 25),
                                      v=self.current_response.headers[header]))

    def do_response_url(self, args):
        self.shell.print_line(self.current_response.url)

    def do_response_body(self, args):
        self.shell.print_raw(self.current_response.body)

    def do_response_status_code(self, args):
        self.shell.print_line(self.current_response.code)

    def do_response_encoding(self, args):
        self.shell.print_line(self.current_response.encoding)

    def do_response_extract_page_title(self, args):
        self.shell.print_line(self.current_response.page_title)

    def do_response_extract_rss_feeds(self, args):
        for url in self.current_response.rss_feeds:
            self.shell.print_line(url)

    def do_response_extract_anchors(self, args):
        for url in self.current_response.anchors:
            self.shell.print_line(url)

    def do_response_extract_titles(self, args):
        for t in self.current_response.titles:
            if len(t['content']) > 0:
                self.shell.print_line('%s: %s' % (t['tag'], t['content']))

    def do_response_extract_hosts(self, args):
        hosts = ['http://{0}'.format(urlparse.urlparse(url).hostname)
                        for url in self.current_response.anchors]
        for host in sorted(set(hosts)):
            self.shell.print_line(host)

    def do_response_xpath_query(self, args):
        for element in self.current_response.xpath_query(' '.join(args)):
            self.shell.print_line(element)

    def do_response_css_select(self, args):
        for element in self.current_response.css_select(' '.join(args)):
            self.shell.print_line(element)

    def do_clear_response(self, args):
        try:
            del(self.current_response)
        except:
            pass

    def __str__(self):
        try:
            return 'mod-http: {data}'.format(data=str(self.current_response))
        except:
            return 'mod-http: <no-data>'

