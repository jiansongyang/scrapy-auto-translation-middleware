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
	    name = "cities"
	    start_url = ["http://some.citydata.website",]
	    def parse(self, response, **kwargs):
		    name = response.xpath("path.to.city.name").get()
		    

 
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTIzMDA5MTg0NywtMTE4MjMxNTk5OSwtOD
k5MDkyMzg4LDEwMDU5MTkzODIsLTE0NjMwNjc4MjksNzAzNTMy
NywtOTg3OTIxNzMsLTIxMDMxNTgxMzcsLTg4NTQ4OTI2XX0=
-->