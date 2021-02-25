from beritascrap.spider_base.detik_spider_base import DetikSpiderBase


class DetikSportSpider(DetikSpiderBase):
    name = 'detik-sport'
    allowed_domains = ['sport.detik.com']
    url_index = "https://sport.detik.com/indeks/"
