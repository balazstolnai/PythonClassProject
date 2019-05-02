# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import OhhItem
from ..Stringer import Stringer


class PokSpider(CrawlSpider):
    name = 'pok'
    mainurl = 'www.origo.hu'

    allowed_domains = [mainurl]
    start_urls = ['https://www.origo.hu/index.html']

    def __init__(self, out_file=name + '.csv', *args, **kwargs):
        self.out_file = out_file
        super(PokSpider, self).__init__(*args, **kwargs)

    rules = (
        Rule(
            LinkExtractor(),
            callback="parse", follow=True),)

    def parse(self, response):
        for article_url in response.xpath(".//div[@class='news-wrap wrap-67-33 normal']").extract():

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
        stringer = Stringer()
        item['title'] = response.xpath('.//title/text()').get()
        item['article_lead'] = stringer.maketext(response.xpath('//div[@class="article-lead"]/p').extract())
        item['text'] = stringer.maketext((response.xpath('//div[@id="article-text"]/p').extract()))

        yield item
