"""
guardiannewsapi.py

"""

import urllib
import urllib2
import json


class GuardianNews(object):
    """
    Service for Guardian News API
    """

    base_url = 'http://content.guardianapis.com/search'

    def __init__(self, key):
        """
        Constructor

        Args:
            key: -string- guardian news api key
        """

        self._key = key

    def build_url(self, **params):
        """
        Contruct a guardian news api url

        Args:
            params -dict- optional key value pair used as query string.
        Returns:
            URL
        """

        querystring = urllib.urlencode(params)
        return '%s?%s' % (self.base_url, querystring)

    def request(self, **params):
        """
        Main method for http request,

        Args:
            params -dict- optional key value pair used as query string.
        Returns:
            response dict.
        """

        defaults = {'api-key': self._key}
        defaults.update(params)

        url = self.build_url(**defaults)

        request = urllib2.Request(url)
        response = urllib2.urlopen(request).read()

        return json.loads(response)

    def fetch_latest_news_articles(self, query, number=10):
        """
        fetches the latest news with the search query
        Args:
            query -string- search keyword.
        """

        defaults = {
            'order-by': 'newest',
            'page-size': number,
            'q': query
        }

        return self.request(**defaults)
