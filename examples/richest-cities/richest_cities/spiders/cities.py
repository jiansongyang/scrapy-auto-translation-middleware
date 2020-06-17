import scrapy
import re
from .. import items
from w3lib.html import remove_tags

class PopulousCities(scrapy.Spider):
    name = "richest-cities"

    start_urls = [
        'https://www.forbes.com/sites/cartercoudriet/2019/03/07/richest-cities-in-the-world-the-top-10-cities-with-the-most-billionaires/'
    ]
    def parse(self, response, **kwargs):

        for h2 in response.xpath('//h2')[1:]:
            title_str = remove_tags(h2.get())
            total_net_str = remove_tags(h2.xpath('following-sibling::p')[0].get())
            richest_resident_str = remove_tags(h2.xpath('following-sibling::p')[1].get())
            desc = remove_tags(h2.xpath('following-sibling::p')[2].get())

            rank, name_en, billionaires = re.match('([0-9]+)*\. *(.*), *([0-9]+) billionaires.*', title_str).groups()
            total_net, = re.match('[Tt]otal net worth: *\$([0-9\.]+) *billion', total_net_str).groups()
            total_net_int_str = str(int(float(total_net)*1000000000))
            richest_res, richest_res_worth = re.match('[Rr]ichest [Rr]esident: (.*), *\$([0-9\.]+) *billion', richest_resident_str).groups()
            richest_res_worth_int = int(float(richest_res_worth)*1000000000)
            yield items.CityItem(
                name_en = name_en,
                rank = int(rank),
                billionaires = int(billionaires),
                total_net_worth_usd = total_net_int_str,
                desc_en = desc,
                richest_resident = richest_res,
                richest_resident_worth = richest_res_worth_int,
            )

