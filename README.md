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

    import scrapy
    class CitySpider(scrapy.Spider):
	    name = "cities"
	    start_url = ["http://some.citydata.website",]
	    def parse(self, response, **kwargs):
		    name = response.xpath("path.to.city.name").get()
		    yield scrapy.Request(url="google.translation.url", cb_kwargs={"name":name})
		def translate(self, response, **kwargs)
		    name = kwargs["name"]
		    name_zh=response.xpath("path.to.name_zh").get()
		    yield items.CityItem(name=name, name_zh=name_zh)
This a apparently much more in tune with Scrapy's design rules but it would be tiresome to introduce extra callback functions just for doing the  translation. Moreover, it would lower down the maintainability and readability of the code.
### option 3: use a translation middleware (best one)
 By making use of a translation middleware you are allowed to do this in the item definition:
 
    import scrapy
    class CityItem(scrapy.Item):
	    name = scrapy.Field()
	    name_zh = scrapy.Field(auto_translate=True, source="name", language="zh")
	    name_fr = scrapy.Field(auto_translate=True, source="name", language="fr") 
	    name_ja = scrapy.Field(auto_translate=True, source="name", language="ja")
	    
In your spider, you just need to populate the original information (the field "name") and the middleware will automatically handle others that are marked as `auto_translate=True`:
     
    ......
    def parse(self, response, **kwargs):
	    ......
	    yield items.CityItem(name="city_name_crawled_from_web")
## installation
To install scrapy-auto-translation-middleware, run:

    pip install scrapy-auto-translation-middleware

<!--stackedit_data:
eyJoaXN0b3J5IjpbLTg1Mjc0MDg0NywtMTIzODE5MTQyOSw2Nj
k4OTc1NCwxNzIxNDMzOTAwLDE0Mjc3NjQ5NDIsMTU0ODU4MTc0
MiwtNjg0MDc1NDY5LDYxNjI0MTg3OSw1NjA5MDQ1OSwtMjAyNj
k5NzU4NSwtMjMwMDkxODQ3LC0xMTgyMzE1OTk5LC04OTkwOTIz
ODgsMTAwNTkxOTM4MiwtMTQ2MzA2NzgyOSw3MDM1MzI3LC05OD
c5MjE3MywtMjEwMzE1ODEzNywtODg1NDg5MjZdfQ==
-->