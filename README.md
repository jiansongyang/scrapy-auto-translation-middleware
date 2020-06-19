# scrapy-auto-translation-middleware

In many circumstances you may want to automatically translate an Item field into another language, and write it into another field. For example, you have defined an Item:

    class City(scrapy.Item):
	    name = scrapy.Field()
	    total_area = scrapy.Field()
	    per_capita_gdp = scrapy.Field()
	    time_zone = scrapy.Field()

The meanings are pretty straight forward. Let's assume you want the name field to be translated into some other languages, say, French, Simplfied Chinese, Japanese, by sending translation requests to Google Translation service. You obviously have an option to do this:
### Option 1:  do the translation in the spider (the worst approach)
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
### Option 2: send a dedicated request to Google to finish the translation (much better, but tedious)
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
### Option 3: use a translation middleware (best one)
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
## Settings
Scrapy-auto-translation-middleware provides built-in support for Google Translation. If you are happy with it, add the following code into your project's settings.py file:

    SPIDER_MIDDLEWARES = {
        scrapy_auto_trans.spidermiddlewares.autotrans.GoogleAutoTranslationMiddleware': 701
    }
Google Translation requires an API Key for each translation service request so you need to specify the key in the settings.py as well:

    GOOGLE_CLOUD_API_KEY="<api.key.you.got.from.google.cloud>"
If you don't feel comfortable to hard-code your API key in settings.py, another option is to specify the key as a command line option when you run the spider:

    scrapy crawl cities -s GOOGLE_CLOUD_API_KEY="<api.key.you.got.from.google.cloud>"
## Define your items
scrapy-auto-translation-middleware will be triggered if you set `auto_translation=True` in the item field definition:

    class CityItem(scrapy.Item):
        name = scrapy.Field()
        name_zh = scrapy.Field(auto_translation=True, source='name', language='zh')
You must specify **source** and **language** in the field definition. They are pretty straight forward in their meanings.
Optionally,         


## Write your own translation middleware

 

<!--stackedit_data:
eyJoaXN0b3J5IjpbODAwMTI5ODQ2LC0xMzQxMjkzODkzLC0xNj
U0ODY2NTYzLDE3Mzk2MDU3MTcsLTEyMzgxOTE0MjksNjY5ODk3
NTQsMTcyMTQzMzkwMCwxNDI3NzY0OTQyLDE1NDg1ODE3NDIsLT
Y4NDA3NTQ2OSw2MTYyNDE4NzksNTYwOTA0NTksLTIwMjY5OTc1
ODUsLTIzMDA5MTg0NywtMTE4MjMxNTk5OSwtODk5MDkyMzg4LD
EwMDU5MTkzODIsLTE0NjMwNjc4MjksNzAzNTMyNywtOTg3OTIx
NzNdfQ==
-->