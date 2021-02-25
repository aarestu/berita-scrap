from beritascrap.spider_base.detik_spider_base import DetikSpiderBase


class DetikTravelSpider(DetikSpiderBase):
    name = 'detik-travel'
    allowed_domains = ['travel.detik.com']
    url_index = "https://travel.detik.com/indeks/"
