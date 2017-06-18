from modules.datamodel import MetaArticle
from typing import List, Dict
from modules.config import SourceSite


class Analyzer(object):
    def __init__(self, feeds: Dict[SourceSite, List[MetaArticle]]):
        self.feeds = feeds

    def get_keywords_count(self) -> dict:
        """
        Analyze keywords, their counts and occurence.
        :return: dict
         {
            "keyword": {
                "count": x,
                "sources": [],
                "positions": [
                    [i, j, k]
                ]
            }
        }
        """
        keywords = {}
        for i, feed in self.feeds.items():
            for j, article in enumerate(feed):
                for k, word in enumerate(article.keywords + article.title + article.perex):
                    if word in keywords:
                        keywords[word]['count'] += 1
                    else:
                        keywords[word] = {
                            'count': 1,
                            'sources': [],
                            'positions': []
                        }

                    if article.source not in keywords[word]['sources']:
                        keywords[word]['sources'].append(article.source)

                    keywords[word]['positions'].append([i, j, k])
        return keywords

    def get_morst_relevant_data(self, keywords: Dict) -> Dict:
        """
        Get most relevant data based on keyword analysis and intersection of keywords
        :param keywords: from get_keywords_count
        :return: Dict with trending keywords, trending articles and and the best article
        """
        most_sources_keywords = {}

        max_sources = 0
        for word, keyword in keywords.items():
            max_sources = len(keyword['sources']) if len(keyword['sources']) > max_sources else max_sources

        for word, keyword in keywords.items():
            if len(keyword['sources']) == max_sources:
                most_sources_keywords[word] = keyword

        trending_keywords = most_sources_keywords.keys()

        trending_articles = []
        for word, keyword in most_sources_keywords.items():
            for position in keyword['positions']:
                trending_articles.append(self.feeds[position[0]][position[1]])
        trending_articles = set(list(trending_articles))

        max_intersect = 0
        best_article = None

        for article in trending_articles:
            intersect = len(set(article.keywords).intersection(trending_keywords))
            if intersect > max_intersect:
                max_intersect = intersect
                best_article = article

        return {
            "trending_keywords": trending_keywords,
            "trending_articles": trending_articles,
            "best_article": best_article
        }
