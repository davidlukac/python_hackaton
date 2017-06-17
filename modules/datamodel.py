from typing import List

from modules.rss import RssArticle
from modules.utils import StringUtils


class MetaArticle(object):
    """ Meta representation of an article, in which all key fields are parsed to lowercase strings without accents.
    """
    def __init__(self, title: List[str], url: str, keywords: List[str], perex: List[str], body: str):
        self.title = title
        self.url = url
        self.keywords = keywords
        self.perex = perex
        self.body = body


class MetaArticleFactory(object):
    @staticmethod
    def from_rss_article(a: RssArticle) -> MetaArticle:
        return MetaArticle(
            StringUtils.to_low_encoded_list(a.title),
            a.url,
            a.keywords,
            StringUtils.to_low_encoded_list(a.perex),
            a.body
        )


class SourceSite(object):
    def __init__(self, machine_name: str, name: str, url: str):
        self.machine_name = machine_name
        self.name = name
        self.url = url

    def __repr__(self):
        return '%s (%s) @ %s' % (self.name, self.machine_name, self.url)
