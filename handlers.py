"""
    handlers.py
"""
import os
from tornado import web
from utils import GuardianNews

GUARDIAN_NEWS_API = GuardianNews(os.environ.get('GUARDIAN_NEWS_KEY'))


class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("index.html", news=None)

    def post(self):
        keyword = self.get_argument('keyword')
        news = GUARDIAN_NEWS_API.fetch_latest_news_articles(keyword)
        self.render("index.html", news=news)

