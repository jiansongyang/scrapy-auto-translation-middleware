import scrapy
import urllib
import pytz
from .. import items
from datetime import datetime

class CitySpider(scrapy.Spider):
    name = "cities"

    def start_requests(self):
        for city in ('hong_kong',):
            url = 'https://www.indexmundi.com/{city}/'.format(city=city)
            yield scrapy.Request(url=url)

    def parse(self, response, **kwargs):
        name = response.xpath('/html/body/table[2]/tr[1]/td[2]/div/div[3]/table/tbody/tr[1]/th/div[1]/text()').get()
        total_area = response.xpath('/html/body/table[2]/tr[1]/td[2]/div/div[3]/table/tbody/tr[32]/td/text()').get()
        gdp = response.xpath('/html/body/table[2]/tr[1]/td[2]/div/div[3]/table/tbody/tr[43]/td/text()').get()
        currency = response.xpath('/html/body/table[2]/tr[1]/td[2]/div/div[3]/table/tbody/tr[47]/td/a[2]/text()').get()
        iso3166_code = response.xpath('/html/body/table[2]/tr[1]/td[2]/div/div[3]/table/tbody/tr[53]/td/div/ul/li[1]/a/text()').get()
        time_zone = pytz.country_timezones[iso3166_code][0]
        current_local_time = datetime.now(tz=pytz.timezone(time_zone)).strftime('%Y-%m-%d %H:%M:%S')

        background_url = response.xpath('/html/body/table[2]/tr[1]/td[1]/ul[1]/li/a').attrib['href']
        url = urllib.parse.urljoin(response.url, background_url)

        item = items.CityItem(
            name=name,
            total_area = total_area,
            gdp = gdp,
            time_zone = time_zone,
            current_local_time = current_local_time,

        )
        yield scrapy.Request(
            url = url,
            callback = self.parse_details,
            cb_kwargs = {'item':  item},

        )

    def parse_details(self, response, **kwargs):
        item = kwargs['item'].copy()
        item['background'] = response.xpath('/html/body/div[4]/div[2]/div[1]/div/text()').get().strip()
        
        yield item
        

