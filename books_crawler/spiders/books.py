# -*- coding: utf-8 -*-
import os
import glob
from scrapy import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.loader import ItemLoader
from books_crawler.items import BooksCrawlerItem


class BooksSpider(Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com']

    # Scrapy arguments to isolate specific segments of a page (i.e., categories)
    # def __init__(self, category):
    #     self.start_urls = [category]

    def parse(self, response):
        # Get list of all books on the page
        books = response.xpath('//h3/a/@href').extract()
        for book in books:
            absolute_url = response.urljoin(book)
            yield Request(absolute_url, callback=self.parse_book)

        # process next page
        next_page_url = response.xpath('//a[text()="next"]/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)
        yield Request(absolute_next_page_url)

    def parse_book(self, response):
        '''
        Scrapes a site and downloads images for all the books and renames the
        images to the title.
        '''
        l = ItemLoader(item=BooksCrawlerItem(), response=response)

        title = response.xpath('//h1/text()').extract_first()
        price = response.xpath('//*[@class="price_color"]/text()').extract_first()
        image_urls = response.xpath('//img/@src').extract_first()
        image_urls = image_urls.replace('../..', 'http://books.toscrape.com')
        rating = response.xpath('//*[contains(@class, "star-rating")]/@class').extract_first()
        rating  = rating.replace('star-rating ', '')
        description = response.xpath('//*[@id="product_description"]/following-sibling::p/text()').extract_first()
        description = description.replace(' ...more', '')

        # Product information table
        upc = product_table(response, 'UPC')
        price_excl = product_table(response, 'Price (excl. tax)')
        price_incl = product_table(response, 'Price (incl. tax)')
        tax = product_table(response, 'Tax')
        p_type = product_table(response, 'Product Type')
        stock = product_table(response, 'Availability')
        reviews = product_table(response, 'Number of reviews')

        l.add_value('title', title)
        l.add_value('price', price)
        l.add_value('image_urls', image_urls)
        l.add_value('rating', rating)
        l.add_value('description', description)
        l.add_value('upc', upc)
        l.add_value('price_excl', price_excl)
        l.add_value('price_incl', price_incl)
        l.add_value('tax', tax)
        l.add_value('p_type', p_type)
        l.add_value('stock', stock)
        l.add_value('reviews', reviews)

        return l.load_item()

        # def close(self, reason):
        #     # calculate latest file generated in root directory
        #     csv_file = max(glob.iglob('*.csv'), key=os.path.getctime)
        #     os.rename(csv_file, 'foobar.csv')

def product_table(response, value):
    return response.xpath('//th[text()="'+value+'"]/following-sibling::td/text()').extract_first()
