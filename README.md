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

    from some.google.translation.lib import Translator
    Class CitySpider(scrapy.Spider):
	    name = "cities"
	    start_url = ["http://some.citydata.website",]
	    def parse(self, response, **kwargs):
		    name = response.xpath("path.to.city.name").get()
		    translator=Translator()
		    name_zh=translator.translate(name, source="en", dest="zh-CN")
This is a bad idea 
 
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTU3ODY1MDQwNSwtMjMwMDkxODQ3LC0xMT
gyMzE1OTk5LC04OTkwOTIzODgsMTAwNTkxOTM4MiwtMTQ2MzA2
NzgyOSw3MDM1MzI3LC05ODc5MjE3MywtMjEwMzE1ODEzNywtOD
g1NDg5MjZdfQ==
-->