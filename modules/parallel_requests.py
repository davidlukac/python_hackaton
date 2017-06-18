from typing import List

import grequests
from grequests import AsyncRequest
from requests import RequestException, Response


class ParallelRequests(object):
    URLS = [
        'http://s.sme.sk/r-rss/20558527/komentare.sme.sk/masaker-sa-zacina-pred-breznom.html',
        'http://s.sme.sk/r-rss/20561414/svet.sme.sk/poziar-v-londyne-obeti-ma-byt-najmenej-58.html',
        'http://s.sme.sk/r-rss/20559883/plus.sme.sk/sefka-dizajnerov-ikea-zbytocne-nas-kopiruju-vieme-to-urobit'
        '-aj-inak.html',
        'http://s.sme.sk/r-rss/20560445/ekonomika.sme.sk/uz-kazda-desiata-materska-putuje-otcovi-peniaze-su'
        '-lakadlom.html',
        'http://s.sme.sk/r-rss/20561282/svet.sme.sk/sedem-veci-ktore-mozu-zrutit-mur-donalda-trumpa.html',
        'http://s.sme.sk/r-rss/20559902/komentare.sme.sk/taky-je-trend-v-stavebnictve-setri-sa-kde-sa-da-a'
        '-fuserstvo-prekvita.html',
        'http://s.sme.sk/r-rss/20556155/sport.sme.sk/stadion-krestovskij-v-petrohrade.html',
        'http://s.sme.sk/r-rss/20561266/komentare.sme.sk/trump-mozno-kube-pomoze-aj-ked-mu-v-skutocnosti-ide-o'
        '-seba.html',
        'http://s.sme.sk/r-rss/20559821/plus.sme.sk/boli-sme-vo-svedskom-almhulte-kde-ma-gigant-ikea-vsetko.html',
        'http://s.sme.sk/r-rss/20560671/svet.sme.sk/kalifat-konci-bojisko-syria-nie-kazda-mocnost-vidi-buducnost'
        '-krajiny-inak.html',
        'http://s.sme.sk/r-rss/20560502/kultura.sme.sk/tereza-nvotova-nasilie-nepachaju-len-sexualni-predatori.html'
    ]

    @classmethod
    def main(cls, urls: List[str]):
        def exception_handler(request: AsyncRequest, exception: RequestException) -> None:
            print("Request for '%s' failed. Error: [%s]" % (request.url, exception))

        def get_responses(url_list: List[str]) -> List[Response]:
            rs = (grequests.get(u) for u in url_list)
            return grequests.imap(rs, exception_handler=exception_handler)

        responses = get_responses(urls)

        for response in responses:
            print('[%s] %s' % (response.status_code, response.url))


if __name__ == '__main__':
    URLS2 = [
        'http://www.heroku.com',
        'http://python-tablib.org',
        'http://httpbin.org',
        'http://python-requests.org',
        'http://fakedomain/',
        'http://kennethreitz.com'
    ]
    prt = ParallelRequests()
    prt.main(ParallelRequests.URLS)
    prt.main(URLS2)
