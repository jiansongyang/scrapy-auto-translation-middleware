# scrapy-auto-translation-middleware
In many circumstances you may want to automatically translate an Item field into another language, and write it into another field. For example, you have defined an Item:

    class City(scrapy.Item):
	    name = scrapy.Field()
	    total_area = scrapy.Field()
	    per_capita_gdp = scrapy.Field()
	    time_zone = scrapy.Field()

The meaning of 
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTExODIzMTU5OTksLTg5OTA5MjM4OCwxMD
A1OTE5MzgyLC0xNDYzMDY3ODI5LDcwMzUzMjcsLTk4NzkyMTcz
LC0yMTAzMTU4MTM3LC04ODU0ODkyNl19
-->