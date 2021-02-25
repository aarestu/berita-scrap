from beritascrap.spider_base.detik_spider_base import DetikSpiderBase


class DetikOtoSpider(DetikSpiderBase):
    name = 'detik-oto'
    allowed_domains = ['oto.detik.com']
    url_index = "https://oto.detik.com/indeks/"
