from beritascrap.spider_base.detik_spider_base import DetikSpiderBase


class DetikFoodSpider(DetikSpiderBase):
    name = 'detik-food'
    allowed_domains = ['food.detik.com']
    url_index = "https://food.detik.com/indeks/"
