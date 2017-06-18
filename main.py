from pprint import pprint

from modules.config import SourceSite, Sources
from modules.rss import ParserFactory
from modules.datamodel import Collector
from modules.analyzer import Analyzer
from requests import request
from modules.datamodel import MetaArticle

if __name__ == '__main__':
    sources = []
    for source, data in Sources.FEEDS.items():
        sources.append(SourceSite(source, data.get('name', ''), data['rss_url'], data.get('base_url', '')))

    parsers = ParserFactory.get_parsers(sources)

    col = Collector(sources)
    entries = col.collect()

    # Analyze keywords
    analyzer = Analyzer(entries)
    keywords = analyzer.get_keywords_count()
    pprint(keywords)

    # Get data from analyzer.
    data = analyzer.get_morst_relevant_data(keywords)

    # Use the result best article.
    article_result = data['best_article'] # type: MetaArticle
    pprint(article_result)

    slack_message = "What's happening today: {}\n\n{}".format(article_result.orginal.title, article_result.url)
    request('GET', 'https://slack.com/api/chat.postMessage?token=xoxp-87076484640-87088670897-121376898595-f020c7663ad965c5ed1a3722bcec15a8&channel=python-hacks&text={}&pretty=1'.format(slack_message))

    titles = "\n".join([article.orginal.title for article in data['trending_articles']])
    pprint(titles)
    slack_message = "Other trending articles: \n\n{}".format(titles)
    request('GET',
            'https://slack.com/api/chat.postMessage?token=xoxp-87076484640-87088670897-121376898595-f020c7663ad965c5ed1a3722bcec15a8&channel=python-hacks&text={}&pretty=1'.format(
                slack_message))
