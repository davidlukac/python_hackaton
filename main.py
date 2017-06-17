from pprint import pprint

from modules.config import SourceSite, Sources
from modules.rss import ParserFactory
from modules.datamodel import Collector

if __name__ == '__main__':
    sources = []
    for source, data in Sources.FEEDS.items():
        sources.append(SourceSite(source, data.get('name', ''), data['rss_url'], data.get('base_url', '')))

    pprint(sources)

    parsers = ParserFactory.get_parsers(sources)

    pprint(parsers)

    col = Collector(sources)
    pprint(col.collect())
