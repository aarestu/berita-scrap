from beritascrap.spider_base.detik_spider_base import DetikSpiderBase


class DetikHotSpider(DetikSpiderBase):
    name = 'detik-hot'
    allowed_domains = ['hot.detik.com']
    url_index = "https://hot.detik.com/indeks/"
