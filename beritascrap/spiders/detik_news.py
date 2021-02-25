from beritascrap.spider_base.detik_spider_base import DetikSpiderBase


class DetikNewsSpider(DetikSpiderBase):
    name = 'detik-news'
    allowed_domains = ['news.detik.com']
    url_index = "https://news.detik.com/indeks/"
