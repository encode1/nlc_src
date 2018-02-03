# """
# Google Natural Language API Wriapper

# """
from apiclient import discovery
from bs4 import BeautifulSoup
from google.appengine.api import urlfetch


class GoogleNaturalLang(object):
    """
    Service for Google Natural Language API
    """
    def __init__(self, key):
        """
        Constructor

        Args:
            key: -string- guardian news api key
        """
        self._key = key

    def build_client(self):
        """
        Instantiates a client to make calls to the api

        Args:
            none
        Returns:
            Client object
        """
        client = discovery.build('language', 'v1beta1', developerKey=self._key)
        return client

    def build_query_data(self, url):
        """
        Generates website content ,

        Args:
            url -TEXT-
        Returns:
             json document object.
        """
        text = self.extract_content(url)

        data = {
            "encodingType": "UTF32",
            "document": {
                "type": "PLAIN_TEXT",
                "language": "en",
                "content": text,
            },
        }
        return data

    def analyze_sentiment(self, url):
        """
        Run a sentiment analysis request on text.

        Args:
            url -string- url to text to be analysed.
        Returns:
            result -dict-.
        """
        client = self.build_client()

        data = self.build_query_data(url)

        annotations = client.documents().analyzeSentiment(body=data).execute()
        return self.fetch_result(annotations)

    def fetch_result(self, annotations):
        """
        Parsing the response

        Args:
            text -string- text to be analysed.
        Returns: result -Dict-
        """
        score = annotations['documentSentiment']['score']
        magnitude = annotations['documentSentiment']['magnitude']
        polarity = annotations['documentSentiment']['polarity']
        result = {
            'score': score,
            'magnitude': magnitude,
            'polarity': polarity,
            'sentences': annotations['sentences']
        }
        return result

    def extract_content(self, url):
        request = urlfetch.fetch(url)
        response = request.content
        soup = BeautifulSoup(response, "html.parser")
        extracttags = ["code", "script", "pre", "style", "embed", "meta", "button", "span", "label", "a", "footer"]
        text = ""
        for tag in extracttags:
            map(lambda x: x.extract(), soup.findAll(tag))
        for string in soup.stripped_strings:
            text += string.encode('utf-8')
        return text
