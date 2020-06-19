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
This is a bad idea as you are making a synchronous request to Google when you are working in an asynchronous framework (in the case of Scrapy for specific, twisted).  A number of bad things will be resulted:
* The failure of Google Translation work will stop the entire crawling process, thus your spider will be much more vulnerable to unexpected events.
* As you are doing a synchronous work that may take unpredictable length of time, the spider will suffer from low performance (keep in mind that there's only one thread running in the Twisted framework).
* The downloader will not take care of the translation work so the states data will become inaccurate.
### option 2: send a dedicated request to Google to finish the translation (much better, but tedious)
Consider the following:

    enter code here

 
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTY4NDA3NTQ2OSw2MTYyNDE4NzksNTYwOT
A0NTksLTIwMjY5OTc1ODUsLTIzMDA5MTg0NywtMTE4MjMxNTk5
OSwtODk5MDkyMzg4LDEwMDU5MTkzODIsLTE0NjMwNjc4MjksNz
AzNTMyNywtOTg3OTIxNzMsLTIxMDMxNTgxMzcsLTg4NTQ4OTI2
XX0=
-->