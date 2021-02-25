from beritascrap.spider_base.detik_spider_base import DetikSpiderBase


class DetikInetSpider(DetikSpiderBase):
    name = 'detik-inet'
    allowed_domains = ['inet.detik.com']
    url_index = "https://inet.detik.com/indeks/"
