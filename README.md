# scrapy-auto-translation-middleware
In many circumstances you may want to automatically translate an Item field into another language, and write it into another field. For example, you have defined an Item:

    class City(scrapy.Item):
	    name = scrapy.Field()
	    total_area = scrapy.Field()
	    per_capita_gdp = scrapy.Field()
	    time_zone = scrapy.Field()

The meanings are pretty str
<!--stackedit_data:
eyJoaXN0b3J5IjpbMTg5ODIyODU4NiwtMTE4MjMxNTk5OSwtOD
k5MDkyMzg4LDEwMDU5MTkzODIsLTE0NjMwNjc4MjksNzAzNTMy
NywtOTg3OTIxNzMsLTIxMDMxNTgxMzcsLTg4NTQ4OTI2XX0=
-->