# -*- coding: utf-8 -*-
import scrapy


class BooksCrawlerItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    rating = scrapy.Field()
    description = scrapy.Field()
    upc = scrapy.Field()
    price_excl = scrapy.Field()
    price_incl = scrapy.Field()
    tax = scrapy.Field()
    p_type = scrapy.Field()
    stock = scrapy.Field()
    reviews = scrapy.Field()
