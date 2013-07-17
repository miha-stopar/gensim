# this script is slightly modified code from https://github.com/richardasaurus/wiki-api (some lines not needed for 
# LSA were removed to fasten the execution)
from pyquery import PyQuery
import requests
import re
import logging

uri_scheme = 'http'
api_uri = 'wikipedia.org/w/api.php'
article_uri = 'wikipedia.org/wiki/'

#common sub sections to exclude from output
unwanted_sections = [
    'External links',
    'Navigation menu',
    'See also',
    'References',
    'Further reading',
    'Contents',
    'Official',
    'Other',
    'Notes',
]

class WikiApi:

    def __init__(self, options=None):
        if options is None:
            options = {}

        self.options = options
        if 'locale' not in options:
            self.options['locale'] = 'en'
        requests_log = logging.getLogger("requests")
        requests_log.setLevel(logging.WARNING)

    def get_article(self, title):
        url = '{0}://{1}.{2}{3}'.format(uri_scheme, self.options['locale'], article_uri, title)
        html = PyQuery(self.get(url))
        data = dict()

        data['heading'] = html('#firstHeading').text()
        data['full'] = unicode()

        for idx, line in enumerate(html('body').find('h2, p').items()):
            if idx == 0:
                data['full'] += data['heading']

            clean_text = self.strip_text(line.text())
            if clean_text:
                data['full'] += '\n\n' + clean_text
        data['full'] = data['full'].strip()
        return data['full']

    def get(self, url):
        r = requests.get(url)
        return r.content

    # remove unwanted information
    def strip_text(self, string):
        #remove citation numbers
        string = re.sub(r'\[\s\d+\s\]', '', string)
        #remove wiki text bold markup tags
        string = re.sub(r'"', '', string)
        #correct spacing around fullstops + commas
        string = re.sub(r' +[.] +', '. ', string)
        string = re.sub(r' +[,] +', ', ', string)
        #remove sub heading edits tags
        string = re.sub(r'\s*\[\s*edit\s*\]\s*', '\n', string)
        #remove unwanted areas
        string = re.sub("|".join(unwanted_sections), '', string, re.IGNORECASE)
        return string

if __name__ == "__main__":
    wiki = WikiApi()
    #wiki = WikiApi({'locale':'de'})
    content = wiki.get_article("Barack Obama")
    print len(content)
    