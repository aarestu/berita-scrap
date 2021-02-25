import re
from datetime import datetime, timedelta

import scrapy
from newspaper import Article
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor

from beritascrap.items import BeritaItem


class DetikSpiderBase(scrapy.Spider):
    url_index = 'https://detik.com/indeks'
    allowed_domains = ['detik.com']
    re_url_article = r"detik\.com/[\w\-]+/d\-\d+/.*"
    re_url_index = r"detik\.com\/indeks(?:\/\d*)?(?:\?.*)?$"

    def __init__(self, start_date=datetime.now().strftime("%Y-%m-%d"), end_date=None, *args, **kwargs):
        super(DetikSpiderBase, self).__init__(*args, **kwargs)

        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        if end_date:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        else:
            end_date = start_date
        if start_date > end_date:
            raise ValueError("Invalid start and end date")

        for day in range((end_date - start_date).days + 1):
            date_ = start_date + timedelta(days=day)
            self.start_urls.append(self.url_index + "?date=" + date_.strftime("%m/%d/%Y"))

    def parse(self, response, **kwargs):

        if re.findall(self.re_url_article, response.url):
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

        if re.findall(self.re_url_index, response.url):

            for page_url in LxmlLinkExtractor(tags=('a', 'area', "article"),
                                              attrs=('href', "i-link"),
                                              allow=[self.re_url_article],
                                              allow_domains=self.allowed_domains).extract_links(response):
                url = page_url.url + "?single=1"

                yield scrapy.Request(response.urljoin(url))

            for page_url in LxmlLinkExtractor(allow=[self.re_url_index],
                                              allow_domains=self.allowed_domains).extract_links(response):
                url = page_url.url

                yield scrapy.Request(response.urljoin(url))
