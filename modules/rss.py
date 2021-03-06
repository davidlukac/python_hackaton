import importlib
import ssl
from abc import ABC, abstractmethod
from pprint import pprint
from typing import Dict, List
from bs4 import BeautifulSoup

import feedparser

from modules.config import SourceSite, Sources
from modules.rss_model import RssArticle


class AbstractRssParser(ABC):
    KEY_KEYWORD = 'keywords'

    def __init__(self, source: SourceSite):
        self.source = source
        if hasattr(ssl, '_create_unverified_context'):
            ssl._create_default_https_context = ssl._create_unverified_context

    @abstractmethod
    def parse(self) -> List[RssArticle]:
        doc = feedparser.parse(self.source.rss_url)
        entries = doc['entries']
        res = []
        for entry in entries:
            title = entry.get('title', '')
            url = entry.get('link', '')
            keywords = entry.get(self.KEY_KEYWORD, [])
            perex = BeautifulSoup(entry.get('description', ''), 'lxml').text.strip()
            res.append(RssArticle(title, url, keywords, perex, '', self.source))
        return res

    def __repr__(self):
        return 'RSS Parser for %s' % self.source.name


class SmeParser(AbstractRssParser):
    KEY_KEYWORD = 'tags'

    def __init__(self, source: SourceSite):
        super().__init__(source)

    def parse(self) -> List[RssArticle]:
        return super().parse()


class PravdaParser(AbstractRssParser):
    def __init__(self, source: SourceSite):
        super().__init__(source)

    def parse(self) -> List[RssArticle]:
        return super().parse()


class AktualityParser(AbstractRssParser):
    def __init__(self, source: SourceSite):
        super().__init__(source)

    def parse(self) -> List[RssArticle]:
        return super().parse()


class ParserFactory(object):
    @staticmethod
    def get_parsers(sources: List[SourceSite]) -> Dict[SourceSite, AbstractRssParser]:
        res = {}
        for source in sources:
            parser_class = ParserFactory.get_parser_class(Sources.FEEDS[source.machine_name][Sources.KEY_PARSER])
            res[source] = parser_class(source)
        return res

    @classmethod
    def get_parser_class(cls, name: str):
        return getattr(importlib.import_module(cls.__module__), name)


if __name__ == '__main__':
    _sources = []
    for _source, _data in Sources.FEEDS.items():
        _sources.append(
            SourceSite(_source, _data.get(Sources.KEY_NAME, ''), _data[Sources.KEY_RSS_URL], _data.get(Sources.KEY_BASE_URL, '')))

    _parsers = ParserFactory.get_parsers(_sources)
    for _s, _parser in _parsers.items():
        pprint(_parser.parse())
