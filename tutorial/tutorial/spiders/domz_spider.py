# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import  LinkExtractor


class DomzSpiderSpider(scrapy.Spider):
    name = 'domz_spider'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://news.sina.com.cn/china/']
    #设定要爬去的网页
    rules =( Rule(LinkExtractor(), callback='parse',follow=True ))

    def parse(self, response):
       filename = response.url.split("/")[-2]
       with open(filename,"wb") as f:
           f.write(response.body)