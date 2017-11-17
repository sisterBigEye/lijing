# -*- coding: utf-8 -*-
import scrapy


class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['http://www.dmoz.org/Computers/Programming/Languages/Python/Books/']
    start_urls = ['http://http://www.dmoz.org/Computers/Programming/Languages/Python/Books//']

    def parse(self, response):
        pass
