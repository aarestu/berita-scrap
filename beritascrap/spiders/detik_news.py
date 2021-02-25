import re
from datetime import datetime, timedelta

import scrapy
from newspaper import Article
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor

from beritascrap.items import BeritaItem


class DetikNewsSpider(scrapy.Spider):
    name = 'detik-news'
    allowed_domains = ['news.detik.com']

    def __init__(self, start_date=datetime.now().strftime("%Y-%m-%d"), end_date=None,*args, **kwargs):
        super(DetikNewsSpider, self).__init__(*args, **kwargs)

        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        if end_date:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        else:
            end_date = start_date
        if start_date > end_date:
            raise ValueError("Invalid start and end date")

        for day in range((end_date - start_date).days + 1):
            date_ = start_date + timedelta(days=day)
            self.start_urls.append('https://news.detik.com/indeks/?date=' + date_.strftime("%m/%d/%Y"))

    def parse(self, response):

        if re.findall(r"detik\.com/\w+/d\-\d+/.*", response.url):
            html = response.text
            article = Article(response.url, language="id")
            article.download(html)
            article.parse()
            item = BeritaItem()
            item["source"] = self.name
            item["title"] = article.title
            item["img"] = article.top_img
            item["text"] = article.text
            item["date"] = article.publish_date
            item["tags"] = article.tags
            item["url"] = article.url
            item["authors"] = article.authors
            yield item

        if re.findall(r"detik\.com/indeks/?\??.*", response.url):

            for page_url in LxmlLinkExtractor(allow=[r"detik\.com/\w+/d\-\d+/.*"],
                                              allow_domains=self.allowed_domains).extract_links(response):
                url = page_url.url + "?single=1"

                yield scrapy.Request(response.urljoin(url))

            for page_url in LxmlLinkExtractor(allow=[r"detik\.com/indeks/\.*"],
                                              allow_domains=self.allowed_domains).extract_links(response):
                url = page_url.url

                yield scrapy.Request(response.urljoin(url))

