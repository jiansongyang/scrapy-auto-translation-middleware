# scrapy-auto-translation-middleware
In many circumstances you may want to automatically translate an Item field into another language, and write it into another field. For example, you have defined an Item:

    class Country(scrapy.Item):
	    name = scrapy.Field()
	    total_area = scrapy.Field()
	    per_capita_gdp = scrapy.Field()
	    time_zone_of_capital_city = scrapy.Field()


<!--stackedit_data:
eyJoaXN0b3J5IjpbMTAwNTkxOTM4MiwtMTQ2MzA2NzgyOSw3MD
M1MzI3LC05ODc5MjE3MywtMjEwMzE1ODEzNywtODg1NDg5MjZd
fQ==
-->