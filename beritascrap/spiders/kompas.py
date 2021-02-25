import re
from datetime import datetime, timedelta

import scrapy
from newspaper import Article
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor

from beritascrap.items import BeritaItem


class KompasSpider(scrapy.Spider):
    name = 'kompas'
    allowed_domains = ['sorot.kompas.com',
                       'kompas.com',
                       'inspirasli.kompas.com',
                       'kilasbumn.kompas.com',
                       'kilasbadannegara.kompas.com',
                       'kolom.kompas.com',
                       'money.kompas.com',
                       'health.kompas.com',
                       'lifestyle.kompas.com',
                       'kilaskorporasi.kompas.com',
                       'www.kompas.com',
                       'www.kompas.id',
                       'balikpapan.kompas.com',
                       'sorotpolitik.kompas.com',
                       'kilaskementerian.kompas.com',
                       'bola.kompas.com',
                       'makassar.kompas.com',
                       'samarinda.kompas.com',
                       'regional.kompas.com',
                       'jeo.kompas.com',
                       'medan.kompas.com',
                       'kilasparlemen.kompas.com',
                       'sbmptn.kompas.com',
                       'genbest.kompas.com',
                       'indeks.kompas.com',
                       'kompas.id',
                       'tekno.kompas.com',
                       'superapps.kompas.com',
                       'travel.kompas.com',
                       'kilaspendidikan.kompas.com',
                       'ohayojepang.kompas.com',
                       'kilasfintech.kompas.com',
                       'kilastransportasi.kompas.com',
                       'kilasbadan.kompas.com',
                       'surabaya.kompas.com',
                       'sains.kompas.com',
                       'nasional.kompas.com',
                       'vik.kompas.com',
                       'entertainment.kompas.com',
                       'edukasi.kompas.com',
                       'megapolitan.kompas.com',
                       'kilasdaerah.kompas.com',
                       'foto.kompas.com',
                       'inside.kompas.com',
                       'internasional.kompas.com',
                       'otomotif.kompas.com',
                       'palembang.kompas.com',
                       'news.kompas.com',
                       'indeks.kompas.com',
                       'properti.kompas.com',
                       'www.kompas.tv']
    start_urls = ['http://kompas.com/']

    url_index = 'https://indeks.kompas.com/?site=all&date='
    re_url_index = r"https:\/\/indeks\.kompas\.com\/\?site=all&date=[\w\-]*(?:&page=\d+)?$"
    re_url_article = r"kompas\.com\/(?:[\w\-]*/)?read\/\d{4}\/\d{2}\/\d{2}\/\d*\/[\w\d\-]*"

    def __init__(self, start_date=datetime.now().strftime("%Y-%m-%d"), end_date=None, *args, **kwargs):
        super(KompasSpider, self).__init__(*args, **kwargs)

        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        if end_date:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        else:
            end_date = start_date
        if start_date > end_date:
            raise ValueError("Invalid start and end date")

        for day in range((end_date - start_date).days + 1):
            date_ = start_date + timedelta(days=day)
            self.start_urls.append(self.url_index + date_.strftime("%Y-%m-%d"))

    def parse(self, response, **kwargs):

        if re.findall(self.re_url_article, response.url):
            html: str = response.text

            html: str = re.sub(r"<strong.*?/strong>", "", html)
            html: str = re.sub(r"<span class=\"time-news\".*?/span>", "", html)
            html: str = re.sub(r"Halaman all", "", html)
            html: str = re.sub(r"- Kompas.com", "", html)

            article = Article(response.url, language="id")
            article.download(html)
            article.parse()
            item = BeritaItem()
            item["source"] = self.name
            item["title"] = article.title
            item["img"] = article.top_img
            item["text"] = article.text

            if item["text"][0] == "-":
                item["text"] = item["text"][1:].strip()

            item["date"] = article.publish_date
            item["tags"] = article.tags
            item["url"] = article.url
            item["authors"] = article.authors
            yield item

        if re.findall(self.re_url_index, response.url):
            for page_url in LxmlLinkExtractor(tags=('a', 'area', "article"),
                                              attrs=('href', "i-link"),
                                              allow=[self.re_url_article],
                                              allow_domains=self.allowed_domains).extract_links(response):
                url = page_url.url + "?page=all"

                yield scrapy.Request(response.urljoin(url))

            for page_url in LxmlLinkExtractor(allow=[self.re_url_index],
                                              allow_domains=[
                                                  "indeks.kompas.com"
                                              ]).extract_links(response):
                url = page_url.url

                yield scrapy.Request(response.urljoin(url))
