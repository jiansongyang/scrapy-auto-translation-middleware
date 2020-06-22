from scrapy.exceptions import UsageError
from scrapy.commands.crawl import Command as CrawlCommand
import scrapy
import re

usage_info = """

Congratulations! 

You have correctly installed scrapy-auto-translation-middelware. The example project will show you how the
middleware will work. 

However, you have to use your own Google Cloud API key for testing purpose. This can be specified by setting GOOGLE_CLOUD_API_KEY
variable in the command line options, like this:

    scrapy crawl {spider} -s GOOGLE_CLOUD_API_KEY=<your-google-cloud-key>

Alternatively, you can specify the key in your settings.py file:

    GOOGLE_CLOUD_API_KEY=<your-google-cloud-key>

For more information about Google Cloud API Key please go to Google Cloud's official website.

Good luck!
"""

class Command(CrawlCommand):
    def process_options(self, args, opts):
        super(Command, self).process_options(args, opts)
        google_key_found = self.settings.get('GOOGLE_CLOUD_API_KEY')
        if not google_key_found:
            raise UsageError(usage_info.format(spider=args[0]))

