# scrapy-auto-translation-middleware

In many circumstances you may want to automatically translate an Item field into another language, and write it into another field. For example, you have defined an Item:

    class City(scrapy.Item):
	    name = scrapy.Field()
	    total_area = scrapy.Field()
	    per_capita_gdp = scrapy.Field()
	    time_zone = scrapy.Field()

The meanings are pretty straight forward. Let's assume you want the name field to be translated into some other languages, say, French, Simplfied Chinese, Japanese, by sending translation requests to Google Translation service. You obviously have an option to do this:
### option 1:  do the translation in the spider (the worst approach)
For example, in your spider:

    Class CitySpider(scrapy.Spider):

 
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTE5Njc0MDA2NDYsLTExODIzMTU5OTksLT
g5OTA5MjM4OCwxMDA1OTE5MzgyLC0xNDYzMDY3ODI5LDcwMzUz
MjcsLTk4NzkyMTczLC0yMTAzMTU4MTM3LC04ODU0ODkyNl19
-->