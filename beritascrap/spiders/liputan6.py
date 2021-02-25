import re
from datetime import datetime, timedelta

import scrapy
from newspaper import Article
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor

from beritascrap.items import BeritaItem


class Liputan6Spider(scrapy.Spider):
    name = 'liputan6'
    allowed_domains = ['liputan6.com/',
                       'www.liputan6.com',
                       'hot.liputan6.com',
                       'belanja.liputan6.com',
                       'surabaya.liputan6.com']
    start_urls = []

    url_index = 'https://www.liputan6.com/indeks/'
    "https://www.liputan6.com/news/indeks/2021/02/25?page=2"
    re_url_index = r"https:\/\/www\.liputan6\.com\/indeks(?:\/\d{4}\/\d{2}\/\d{2})?(?:\?page=\d+)?$"
    re_url_article = r"liputan6\.com\/(?:[\w\-]*/)?read\/\d*\/[\w\d\-]*"

    def __init__(self, start_date=datetime.now().strftime("%Y-%m-%d"), end_date=None, *args, **kwargs):
        super(Liputan6Spider, self).__init__(*args, **kwargs)

        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        if end_date:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        else:
            end_date = start_date
        if start_date > end_date:
            raise ValueError("Invalid start and end date")

        for day in range((end_date - start_date).days + 1):
            date_ = start_date + timedelta(days=day)
            self.start_urls.append(self.url_index + date_.strftime("%Y/%m/%d"))

    def parse(self, response, **kwargs):

        if re.findall(self.re_url_article, response.url):
            html: str = response.text

            html: str = re.sub(r"<strong.*?/strong>", "", html)
            html: str = re.sub(r"<b>Liputan6.com,.{5,15}/b>", "", html)
            html: str = re.sub(r"<p class=\"baca-juga__header.*/p>", "", html)
            html: str = re.sub(r"<ul class=\"baca-juga__list.*/ul>", "", html)

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
                url = page_url.url

                yield scrapy.Request(response.urljoin(url))

            for page_url in LxmlLinkExtractor(allow=[self.re_url_index],
                                              allow_domains=[
                                                  "liputan6.com"
                                              ]).extract_links(response):
                url = page_url.url

                yield scrapy.Request(response.urljoin(url))
