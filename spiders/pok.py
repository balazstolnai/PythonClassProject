# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import OhhItem

class PokSpider(scrapy.Spider):
    name = 'pok'
    mainurl = 'www.gphirek.hu'

    allowed_domains = [mainurl]
    start_urls = ['https://www.gphirek.hu/index.html']

    rules = (
        Rule(
            LinkExtractor(),
            callback="parse", follow=True),)

    def parse(self, response):
        for article_url in response.xpath(".//div[@class='day-news-item']").extract():

            location = article_url.find(self.mainurl)
            location += len(self.mainurl)
            realurl = ''

            betu = article_url[location]

            while betu != '.':
                realurl += betu
                location = location + 1
                betu = article_url[location]

            realurl += '.html'
            yield response.follow(realurl, callback=self.parse_article)

    def parse_article(self, response):
        item = OhhItem()
        item['title'] = response.xpath('.//title/text()').get()
        item['article_lead'] = response.xpath('//div[@class="article-lead"]/p/text()').get()
        item['text'] = ''.join(response.xpath('//div/p[position()>1]/text()').extract())

        return item
