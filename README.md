# scrapy-auto-translation-middleware
In many circumstances you may want to automatically translate an Item field into another language, and write it into another field. For example, you have defined an Item:

    class City(scrapy.Item):
	    name = scrapy.Field()
	    total_area = scrapy.Field()
	    per_capita_gdp = scrapy.Field()
	    time_zone = scrapy.Field()

The meanings are pretty straight forward. Let's assume you want the name field to be translated into some other languages, say, French, Simplfied Chinese, Japanese, by sending translation requests to Google Translation service. Basically you have 
<!--stackedit_data:
eyJoaXN0b3J5IjpbMjc3NTQ3Nzc2LC0xMTgyMzE1OTk5LC04OT
kwOTIzODgsMTAwNTkxOTM4MiwtMTQ2MzA2NzgyOSw3MDM1MzI3
LC05ODc5MjE3MywtMjEwMzE1ODEzNywtODg1NDg5MjZdfQ==
-->