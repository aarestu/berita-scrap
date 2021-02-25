from beritascrap.spider_base.detik_spider_base import DetikSpiderBase


class DetikFinanceSpider(DetikSpiderBase):
    name = 'detik-finance'
    allowed_domains = ['finance.detik.com']
    url_index = "https://finance.detik.com/indeks/"
