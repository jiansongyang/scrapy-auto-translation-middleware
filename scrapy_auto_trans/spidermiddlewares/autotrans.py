"""
Automatically translate specified item fields
"""
import scrapy
from .. import exceptions as execs
from urllib.parse import quote as urlquote, unquote as urlunquote
import requests
import json
import logging

logger = logging.getLogger(__name__)

class AutoTranslationMiddlewareBase:

    META_KEY = 'scrapy-auto-translation-middleware'
    DEFAULT_LANGUAGE= 'en'

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.settings = settings

    def get_source_language_code(self, source_field):

        if 'source_language' in source_field:
            return source_field['source_language']

        if self.DEFAULT_LANGUAGE is not None:
            return self.DEFAULT_LANGUAGE

        if self.settings.get('DEFAULT_LANGUAGE') is not None:
            return self.settings.get('DEFAULT_LANGUAGE')

        return 'en'

    def process_spider_output(self, response, result, spider):
        if self.META_KEY in response.request.meta:
            """
            We have somehow translated the item field. Send the result to the engine.
            """
            yield from result
        else:
            for x in result:
                if not isinstance(x, scrapy.Item):
                    yield x
                else:
                    item = x
                    item_class = item.__class__
                    for field_name in item.fields:
                        item_cls_field = item_class.fields[field_name]
                        if item_cls_field.get('auto_translate'):
                            is_critical = item_cls_field.get('critical')
                            try:
                                yield from self._handle_untranslated_item(item, field_name)
                            except execs.TranslationError as e:
                                if is_critical:
                                    raise e
                                else:
                                    logger.warn("Translation Error: %s"%e.message)
                                    yield item

    def _handle_untranslated_item(self, item, target_field_name):
        raise NotImplementedError
            
class SyncAutoTranslationMiddleware(AutoTranslationMiddlewareBase):
    """
    Translate "text" to the language specified by "target_lang_code".
    You need to implement this function only when you choose to go with Synchronous translation.
    Make sure this function is finished real quickly.
    """

    def translate(self, source_lang_code, target_lang_code, text, **kwargs):
        return 'Text translated by SyncAutoTranslationMiddleware. If you see this, please rewrite the ' \
               'SyncAutoTranslationMiddleware.translate() method'

    def _handle_untranslated_item(self, item, target_field_name):
        item_class = item.__class__
        target_field = item_class.fields[target_field_name]


        is_critical = target_field.get('critical')
        source_field = target_field['source_field']
        source_field_value = item[source_field]
        source_field_language = self.get_source_language_code(target_field)
        target_field_name = target_field_name
        target_field_language = target_field.get('target_lang_code')

        logger.debug(
            f"SyncAutoTranslationMiddleware._handle_untranslated_item:\n" \
            f"item: {item_class}\n" \
            f"source_field: {source_field}\n" \
            f"source_field_language: {source_field_language}\n" \
            f"source_field_value: {source_field_value}\n" \
            f"target_field: {target_field_name}\n" \
            f"target_field_language: {target_field_language}\n" \
            f"critical: {is_critical}\n"
        )

        translated_item = item.copy()
        translated_item[target_field_name] = self.translate(
            source_lang_code = source_field_language,
            target_lang_code = target_field_language,
            text = source_field_value
        )

        yield translated_item

    def process_spider_input(self, response, spider):
        pass

    def process_spider_exception(self, response, exception, spider):
        pass

class AsyncAutoTranslationMiddleware(AutoTranslationMiddlewareBase):

    def _handle_untranslated_item(self, item, target_field_name):

        item_class = item.__class__
        target_field = item_class.fields[target_field_name]


        is_critical = target_field.get('critical')
        source_field = target_field['source_field']
        source_field_value = item[source_field]
        source_field_language = self.get_source_language_code(target_field)
        target_field_name = target_field_name
        target_field_language = target_field.get('target_lang_code')

        logger.debug(
            f"AsyncAutoTranslationMiddleware._handle_untranslated_item:\n" \
            f"item: {item_class}\n" \
            f"source_field: {source_field}\n" \
            f"source_field_language: {source_field_language}\n" \
            f"source_field_value: {source_field_value}\n" \
            f"target_field: {target_field_name}\n" \
            f"target_field_language: {target_field_language}\n" \
            f"critical: {is_critical}\n"
        )

        yield scrapy.Request(
            url = self.get_translate_url(
                source_lang_code = target_field.get('source_lang_code') or 'en',
                target_lang_code = target_field.get('target_lang_code'),
                text = item[source_field],
            ),
            meta = {
                'handle_httpstatus_all': True,
                self.META_KEY: {
                    'item': item,
                    'source_field': source_field,
                    'target_field': target_field_name,
                }
            }
        )

    def process_spider_input(self, response, spider):
        if self.META_KEY in response.request.meta:
            if response.status<300:
                raise execs.TranslationResult(response)
            raise execs.TranslationErrorDueToInvalidResponseCode(response)

    def process_spider_exception(self, response, exception, spider):
        if isinstance(exception, execs.TranslationResult):
            """
            Don't be confused, it's not an error. Scrapy only allows us to get the translated result 
            by raising an Exception from process_spider_input()
            """
            trans_result = self.get_translate_result(response)
            item = response.request.meta[self.META_KEY]['item']
            source_field = response.request.meta[self.META_KEY]['source_field']
            target_field = response.request.meta[self.META_KEY]['target_field']
            item[target_field] = trans_result
            logger.debug(
                f"AsyncAutoTranslationMiddleware.process_spider_exception:\n" \
                f"item: {item}\n" 
                f"source_field: {source_field}\n" 
                f"target_field: {target_field}\n" 
            )
            population = self.settings.get('ITEM_FIELD_POPULATION_MANNER')
            if population=='CUMULATIVE':
                yield item
            elif population=='SINGLE_FIELD':
                yield item.__class__(
                    **{source_field: item[source_field], target_field: item[target_field]}
                )
            else:
                yield item

        elif isinstance(exception, execs.TranslationError):
            logger.warn(exception.warn())

    def get_translate_url(self, source_lang_code, target_lang_code, text, **kwargs):
        raise NotImplementedError

    def get_translate_result(self, response, **kwargs):
        raise NotImplementedError

class GoogleAutoTranslationMiddleware(AsyncAutoTranslationMiddleware):
    """
    Asynchronous translator using Google Cloud Translation.
    Please replace the api_key attribute with your own key. 
    Alternatively, in global settings you may define GOOGLE_CLOUD_API_KEY for this purpose.
    If you don't feel comfortable to expose your API key anywhere in the code or settings, 
    you may go with command line option like: 
        scrapy crawl <your-spider-name> -s GOOGLE_CLOUD_API_KEY=<your-google-api-key>
    
    """

    api_key = None

    def get_translate_url(self, source_lang_code, target_lang_code, text, **kwargs):
        quoted_text = urlquote(text.encode('utf8'))
        key = self.get_api_key()
        return \
            f'https://translation.googleapis.com/language/translate/v2?key={key}' \
            f'&q={quoted_text}' \
            f'&target={target_lang_code}' \
            f'&source={source_lang_code}'

    def get_translate_result(self, response, **kwargs):
        return urlunquote(json.loads(response.text)['data']['translations'][0]['translatedText'])

    def get_api_key(self):
        if hasattr(self, 'api_key') and bool(self.api_key):
            return self.api_key

        key = self.settings.get('GOOGLE_CLOUD_API_KEY')
        if key:
            return key
        raise execs.TranslationErrorGeneral(
            "A Google Cloud API Key must be available. "
            + "You may either add an attribute 'api_key' to the class {cls} or its subclass, ".format(cls=self.__class__.__name__)
            + "add a variable 'GOOGLE_CLOUD_API_KEY' in your settings file, "
            + "or specify it as a command line option like this: "
            + "scrapy crawl <your-spider-name> -s GOOGLE_CLOUD_API_KEY=<your-google-cloud-api-key>"
        )
