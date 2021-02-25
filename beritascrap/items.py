# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class BeritaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    title = Field()
    link = Field()
    img = Field()
    category = Field()
    date = Field()
    text = Field()
    url = Field()
    tags = Field()
    authors = Field()
