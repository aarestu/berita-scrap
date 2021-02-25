from beritascrap.spider_base.detik_spider_base import DetikSpiderBase


class DetikHealthSpider(DetikSpiderBase):
    name = 'detik-health'
    allowed_domains = ['health.detik.com']
    url_index = "https://health.detik.com/indeks/"
