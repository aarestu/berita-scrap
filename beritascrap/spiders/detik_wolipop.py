from beritascrap.spider_base.detik_spider_base import DetikSpiderBase


class DetikWolipopSpider(DetikSpiderBase):
    name = 'detik-wolipop'
    allowed_domains = ['wolipop.detik.com']
    url_index = "https://wolipop.detik.com/indeks/"
