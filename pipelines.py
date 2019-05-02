# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pandas as pd
from .items import OhhItem


class OhhPipeline(object):
    def open_spider(self, spider):
        df = pd.DataFrame(columns=OhhItem.fields.keys())
        df.to_csv(spider.out_file, index=False, sep=";")

    def process_item(self, item, spider):
        df = pd.DataFrame(dict(item), columns=item.fields.keys(), index=[0])
        df.to_csv(spider.out_file, index=False, sep=";", mode='a', header=False, encoding="utf-8")
        return item
