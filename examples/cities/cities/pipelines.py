# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.exceptions import DropItem
from scrapy.exporters import JsonItemExporter
from . import items

class CitiesPipeline:

    def open_spider(self, spider):
        self.city = JsonItemExporter(open("cities.json","wb"), encoding='utf-8', indent=2)
        self.city.start_exporting()

    def close_spider(self, spider):
        self.city.finish_exporting()

    def process_item(self, item, spider):
        if isinstance(item, items.CityItem):
            self.city.export_item(item)
            return item
        raise DropItem(item)

