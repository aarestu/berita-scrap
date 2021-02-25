from beritascrap.spider_base.detik_spider_base import DetikSpiderBase


class DetikSepakbolaSpider(DetikSpiderBase):
    name = 'detik-sepakbola'
    allowed_domains = ['sport.detik.com']
    url_index = "https://sport.detik.com/sepakbola/indeks/"

    re_url_article = r"detik\.com/sepakbola/[\w\-]+/d\-\d+/.*"
    re_url_index = r"detik\.com\/sepakbola/indeks(?:\/\d*)?(?:\?.*)?$"
