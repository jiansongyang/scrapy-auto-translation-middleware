# scrapy-auto-translation-middleware
In many circumstances you may want to automatically translate an Item field into another language, and write it into another field. For example, you have defined an Item:

    class Country(scrapy.Item):
	    name = scrapy.Field()
	    total_area = scrapy.Field()
	    per_capita_gdp = scrapy.Field()
	    time_zone = scrapy.Field()


<!--stackedit_data:
eyJoaXN0b3J5IjpbLTE0NjMwNjc4MjksNzAzNTMyNywtOTg3OT
IxNzMsLTIxMDMxNTgxMzcsLTg4NTQ4OTI2XX0=
-->