# Installation

    $ pip install beautifulsoup4
    $ pip install requests

    $ python setup.py install

## On debian (or other)
  
    $ apt-get install python-lxml

# Usage

__Trick__: You can use <TAB> completion and CTRL-R history :)

    $ osint-shell

## HTTP Module

### First! -> Send GET HTTP request

    $ http request_get http://www.lemonde.fr
  
### Retrieve HTTP information

    $ http response_status_code
    $ http response_encoding
    $ http response_headers

### Extract HTML information

    $ http response_extract_page_title
    $ http response_extract_rss_feeds
    $ http response_extract_titles # H1 to H6
    $ http response_extract_anchors
    $ http response_extract_hosts
    $ http response_xpath_query //div[@class='pages']/ul/li/a/text()

## Google Module

    $ google search <your query>
    $ google suggest <your query>

