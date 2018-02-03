"""
    handlers.py
"""
import os
from tornado import web
from models import Article, Sentence
from utils import GuardianNews, GoogleNaturalLang

GUARDIAN_NEWS_API = GuardianNews(os.environ.get('GUARDIAN_NEWS_KEY'))
GOOGLE_NATURAL_LANG_API = GoogleNaturalLang(
    os.environ.get('GOOGLE_NATURAL_LANG_KEY'))


class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("index.html", articleList=[], analysis=None, keyword="")

    def post(self):
        keyword = self.get_argument('keyword')

        articles = GUARDIAN_NEWS_API.fetch_latest_news_articles(keyword)

        Headline_url_dict = {}
        articleAnalysis = {}

        for article in articles:
            url = article['webUrl']
            headline = article['webTitle']
            sentiment_result = GOOGLE_NATURAL_LANG_API.analyze_sentiment(url)

            articleAnalysis.update({url: sentiment_result})

            # Add article to the database
            article = Article.create(
                headline=headline.encode('unicode_escape'),
                url=url.encode('unicode_escape'),
                sentiment_score=articleAnalysis[url]['score'],
                sentiment_polarity=articleAnalysis[url]['polarity'],
                sentiment_magnitude=articleAnalysis[url]['magnitude']
            )
            # Add sentence to the database
            for sentence in sentiment_result['sentences']:
                Sentence.create(
                    text=sentence['text']['content'].encode('unicode_escape'),
                    begin_offset=sentence['text']['beginOffset'],
                    sentiment_score=sentence['sentiment']['score'],
                    sentiment_polarity=sentence['sentiment']['polarity'],
                    sentiment_magnitude=sentence['sentiment']['magnitude'],
                    article=article)

            Headline_url_dict.update({headline: url})

        # articleAnalysis = {
        #     url: GOOGLE_NATURAL_LANG_API.analyze_sentiment(url)
        #     for url in articleList}

        self.render(
            "index.html", articleList=Headline_url_dict,
            analysis=articleAnalysis, keyword=keyword)
