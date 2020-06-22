import scrapy
from . import translators as tr

class CityItem(scrapy.Item):
    """
    City Item definition
    """

    # original information
    name = scrapy.Field()
    background  = scrapy.Field()
    total_area = scrapy.Field()
    gdp = scrapy.Field()
    time_zone = scrapy.Field()
    currency = scrapy.Field()

    # translated information
    name_zh = scrapy.Field(auto_translate=True, source='name', language='zh-CN')
    name_tw = scrapy.Field(auto_translate=True, source='name', language='zh-TW')
    name_ko = scrapy.Field(auto_translate=True, source='name', language='ko')
    name_ja = scrapy.Field(auto_translate=True, source='name', language='ja')
    name_ru = scrapy.Field(auto_translate=True, source='name', language='ru')
    name_fr = scrapy.Field(auto_translate=True, source='name', language='fr')
    name_es = scrapy.Field(auto_translate=True, source='name', language='es')
    name_de = scrapy.Field(auto_translate=True, source='name', language='de')
    name_vi = scrapy.Field(auto_translate=True, source='name', language='vi')

    background_zh = scrapy.Field(auto_translate=True, source='background', language='zh-CN')
    background_tw = scrapy.Field(auto_translate=True, source='background', language='zh-TW')
    background_ko = scrapy.Field(auto_translate=True, source='background', language='ko')
    background_ja = scrapy.Field(auto_translate=True, source='background', language='ja')
    background_ru = scrapy.Field(auto_translate=True, source='background', language='ru')
    background_fr = scrapy.Field(auto_translate=True, source='background', language='fr')
    background_es = scrapy.Field(auto_translate=True, source='background', language='es')
    background_de = scrapy.Field(auto_translate=True, source='background', language='de')
    background_vi = scrapy.Field(auto_translate=True, source='background', language='vi')

    # other types of derived information
    total_area_in_sq_miles = scrapy.Field(auto_translate=True, translate=tr.sqkm2sqmiles, source='total_area')
    current_local_time = scrapy.Field(auto_translate=True, translate=tr.get_time, source='time_zone')
    gdp_in_cny = scrapy.Field(auto_translate=True, translate=tr.usd2foreign('CNY'), source='gdp')
    gdp_in_eur = scrapy.Field(auto_translate=True, translate=tr.usd2foreign('EUR'), source='gdp')
    gdp_in_jpy = scrapy.Field(auto_translate=True, translate=tr.usd2foreign('JPY'), source='gdp')
    

