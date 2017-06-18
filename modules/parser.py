import requests
from lxml import html

from modules.config import SourceSite
from modules.rss import ParserFactory, RssArticle, Sources
from modules.utils import ListUtils
import threading


class MyThread(threading.Thread):
    def __init__(self, obj):
        super().__init__()
        self.obj = obj
        self.result = None

    # Run a thread
    def run(self):
        self.result = self.obj.get_keywords()
        return


class Parser(object):
    @staticmethod
    def get_keywords(document: str) -> list:
        tree = html.fromstring(document)

        keywords = []

        try:
            keywords = tree.xpath('/html/head/meta[@name="keywords"]/@content')[0].split(', ')
        except IndexError:
            pass
        try:
            keywords = tree.xpath('/html/head/meta[@name="news_keywords"]/@content')[0].split(', ')
        except IndexError:
            pass

        return ListUtils.to_low_encoded_list(keywords)


if __name__ == '__main__':
    sources = []
    for source, data in Sources.FEEDS.items():
        sources.append(SourceSite(source, data.get(Sources.KEY_NAME, ''), data[Sources.KEY_RSS_URL], data.get(Sources.KEY_BASE_URL, '')))

    parsers = ParserFactory.get_parsers(sources)

    for source, parser in parsers.items():
        article = next(iter(parser.parse() or []), None)
        if article is not None:
            html_parser = Parser(article)
            print(html_parser.get_keywords())

