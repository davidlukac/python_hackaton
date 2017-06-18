from typing import Dict, List

from grequests import AsyncRequest
from grequests import get, imap
from requests import Response

from modules.config import SourceSite
from modules.parallel_requests import ParallelRequests
from modules.parser import Parser
from modules.rss import ParserFactory
from modules.rss_model import RssArticle
from modules.utils import ListUtils
from modules.utils import StringUtils


class MetaArticle(object):
    """ Meta representation of an article, in which all key fields are parsed to lowercase strings without accents. """

    def __init__(self, title: List[str], url: str, keywords: List[str], perex: List[str], body: str,
                 source: SourceSite, orginal: RssArticle):
        self.title = title
        self.url = url
        self.keywords = keywords
        self.perex = perex
        self.body = body
        self.source = source
        self.orginal = orginal

    def __repr__(self):
        return 'Title: %s\nUrl: %s\nKeywords: %s\nPerex: %s\nBody: %s\nSource: %s' \
               % (self.title, self.url, self.keywords, self.perex, self.body, self.source.name)


class MetaArticleFactory(object):
    @staticmethod
    def from_rss_article(a: RssArticle) -> MetaArticle:
        return MetaArticle(
            title=StringUtils.remove_stopwords(StringUtils.to_low_encoded_list(a.title)),
            url=a.url,
            keywords=StringUtils.remove_stopwords(ListUtils.to_low_encoded_list(a.keywords)),
            perex=StringUtils.remove_stopwords(StringUtils.to_low_encoded_list(a.perex)),
            body=a.body,
            source=a.source,
            orginal=a
        )


class Collector(object):
    def __init__(self, sources: List[SourceSite]):
        self.sources = sources
        self.parsers = ParserFactory.get_parsers(self.sources)

    def collect(self) -> Dict[SourceSite, List[MetaArticle]]:
        res = {}

        def response_hook(response: Response, *request_args, **request_kwargs):
            response.original_request_url = request_args['original_request_url']
            return response

        def exception_handler(request: AsyncRequest, exception: Exception) -> None:
            print("Request for '%s' failed. Error: [%s]" % (request.url, exception))

        # for source, parser in self.parsers.items():
        #     articles = []
        #     keywords = []
        #     rss = []
        #
        #     parsed_articles = parser.parse()
        #
        #     # Start new parser for each Parser
        #     for rss_article in parsed_articles:
        #         html_parser = Parser(rss_article)
        #         t = MyThread(html_parser, rss_article)
        #         threads.append(t)
        #         t.start()

        def get_responses(urls: Dict[str, RssArticle]) -> List[Response]:
            rs = (get(u, hooks={'response': response_hook(original_request_url=u)}) for u, _ in urls.items())
            return imap(rs, exception_handler=exception_handler, size=20)

        for source, parser in self.parsers.items():
            articles = []

            # # Get results from threads
            # for t in threads:
            #     keywords.append(t.result)
            #     rss.append(t.rss)

            rss_articles = parser.parse()
            # Turn list of RSS article to dict {URL: RssArticle}.
            article_urls = {rss_article.url: rss_article for rss_article in rss_articles}  # type: Dict[str, RssArticle]
            # Get Responses for each URL.
            responses = get_responses(article_urls)
            # Turn responses into their content if we got successfully back.
            responses_list = [r for r in responses]
            responses_2 = {response.request.url: response.content for response in responses_list if response.status_code < 400}

            for url, content in responses_2.items():
                print('[%s] %s' % (url, content))
                new_keywords = Parser.get_keywords(content)
                original_article = article_urls[url]
                original_article.keywords += new_keywords

            for i, rss_article in enumerate(rss_articles):
                meta_article = MetaArticleFactory.from_rss_article(rss_article)
                # Match the right keywords for right article
                for i, rs in enumerate(rss):
                    if rs == rss_article:
                        meta_article.keywords += keywords[i] #?

                articles.append(meta_article)
            res[source] = articles

        return res
