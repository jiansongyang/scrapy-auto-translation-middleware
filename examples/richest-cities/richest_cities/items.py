# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_auto_trans import FailureAction

def usd2foreign(currency):
    def _usd(field_name, item, **kwargs):
        def callback(response, _field_name, _item, **cb_kwargs):
            rate_str = response.xpath("//td[re:test(a/@href,'.*%s$')]/a/text()"%currency).get()
            _source_field_name = cb_kwargs['source']
            _source_value = _item[_source_field_name]
            return '%d'%int(float(_source_value)*float(rate_str))

        return scrapy.Request(
            url = 'https://www.x-rates.com/table/?from=USD&amount=1',
            dont_filter=True,
        ), callback

    return _usd

class CityItem(scrapy.Item):

    name_en = scrapy.Field(language='en')
    name_zh = scrapy.Field(auto_translate=True, on_failure=FailureAction.REPORT_IN_FIELD, source='name_en', language='zh')
    name_kr = scrapy.Field(auto_translate=True, on_failure=FailureAction.REPORT_IN_FIELD, source='name_en', language='ko')
    name_jp = scrapy.Field(auto_translate=True, on_failure=FailureAction.REPORT_IN_FIELD, source='name_en', language='ja')
    name_fr = scrapy.Field(auto_translate=True, on_failure=FailureAction.REPORT_IN_FIELD, source='name_en', language='fr')
    name_de = scrapy.Field(auto_translate=True, on_failure=FailureAction.REPORT_IN_FIELD, source='name_en', language='de')

    desc_en = scrapy.Field(language='en')
    desc_zh = scrapy.Field(auto_translate=True, on_failure=FailureAction.REPORT_IN_FIELD, source='desc_en', language='zh')
    desc_kr = scrapy.Field(auto_translate=True, on_failure=FailureAction.REPORT_IN_FIELD, source='desc_en', language='ko')
    desc_jp = scrapy.Field(auto_translate=True, on_failure=FailureAction.REPORT_IN_FIELD, source='desc_en', language='ja')
    desc_fr = scrapy.Field(auto_translate=True, on_failure=FailureAction.REPORT_IN_FIELD, source='desc_en', language='fr')
    desc_de = scrapy.Field(auto_translate=True, on_failure=FailureAction.REPORT_IN_FIELD, source='desc_en', language='de')

    total_net_worth_usd = scrapy.Field()
    total_net_worth_cny = scrapy.Field(auto_translate=True, source='total_net_worth_usd',translate=usd2foreign('CNY'))
    total_net_worth_jpy = scrapy.Field(auto_translate=True, source='total_net_worth_usd',translate=usd2foreign('JPY'))
    total_net_worth_krw = scrapy.Field(auto_translate=True, source='total_net_worth_usd',translate=usd2foreign('KRW'))
    total_net_worth_eur = scrapy.Field(auto_translate=True, source='total_net_worth_usd',translate=usd2foreign('EUR'))
    total_net_worth_rub = scrapy.Field(auto_translate=True, source='total_net_worth_usd',translate=usd2foreign('RUB'))

    rank = scrapy.Field()
    billionaires = scrapy.Field()
    richest_resident = scrapy.Field()
    richest_resident_worth = scrapy.Field()


