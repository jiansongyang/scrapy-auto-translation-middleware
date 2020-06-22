"""
Translator functions are all defined here.
A translator is simply a function (or callable) that takes field_name and item as the parameters, and returns the 
translated field value or a tuple of (request, callback_function).
If a (request, callback_function) is returned, the callback function is expected to take response, field_name, item
as the paremeters, and to return the translated value or another (request, callback_function) tuple.
"""

from pytz import timezone
from datetime import datetime
import scrapy
import re

def sqkm2sqmiles(field_name, item, **kwargs):
    """
    Convert square killometers to square miles
    """
    sqkm_field = kwargs['source']
    sqkm = item[sqkm_field].replace(',','')
    return '{:,}'.format(int(float(sqkm)*0.386102159))

def get_time(field_name, item, **kwargs):
    """
    Get the current datetime value of the specified timezone
    """
    tz_field = kwargs['source']
    tz_name = item[tz_field]
    tz = timezone(tz_name)
    return datetime.now(tz=tz).strftime('%Y-%m-%d %H:%M:%S')

def usd2foreign(currency):
    def _usd(field_name, item, **kwargs):
        def callback(response, _field_name, _item, **cb_kwargs):
            rate_str = response.xpath("//td[re:test(a/@href,'.*%s$')]/a/text()"%currency).get()
            _source_field_name = cb_kwargs['source']
            _source_value_raw = _item[_source_field_name]
            value_str, unit = re.match(' *[^0-9]*([0-9\.]+) +([a-z]+) *', _source_value_raw).groups()[0:2]
            trans_value = int(float(value_str)*float(rate_str))
            return '{} {:,} {}'.format(currency, trans_value, unit)

        return scrapy.Request(
            url = 'https://www.x-rates.com/table/?from=USD&amount=1',
            dont_filter=True,
        ), callback

    return _usd
