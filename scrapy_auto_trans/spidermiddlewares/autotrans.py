"""
Automatically translate specified item fields
"""
import scrapy
import types
from .. import exceptions as excs
from .. import FailureAction
from urllib.parse import quote as urlquote, unquote as urlunquote
import requests
import json
import logging

logger = logging.getLogger(__name__)

class AutoTranslationMiddlewareBase:

    META_KEY = 'scrapy-auto-translation-middleware'
    TAG = 'auto_translate'
    DEFAULT_LANGUAGE= 'en'
    IN_FIELD_ERROR_MSG = '--- translation error ---'

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.settings = settings

    def process_spider_output(self, response, result, spider):

        for x in result:
            if isinstance(x, (dict, scrapy.Request)):
                yield x
            elif isinstance(x, scrapy.Item):
                item = x
                count_field_auto_trans = len([(k,v)for k,v in item.fields.items() if self.TAG in v ])
                if count_field_auto_trans==0:
                    """
                    It's a brand new item but no fields are to be translated, let's yield it
                    """
                    yield item
                else:
                    """
                    It's time for us to play on the stage
                    """
                    trans_result = self.handle_untranslated_item(item)
                    # hopefully trans_result is a new request containing item in its meta data
                    yield trans_result
            else:
                yield x

    def handle_untranslated_item(self, item):
        """
        Either returns the item or a new request that contains the item in its meta data
        """
        new_item = item.copy()
        for field_name in item.fields:
            if field_name not in item and item.fields[field_name].get(self.TAG):
                """
                A new target field that's yet to be translated
                """
                target_field = item.fields[field_name]
                source_field_name = target_field['source']
                kwargs = target_field.copy()
                kwargs.pop(self.TAG)
                if 'translate' in target_field:
                    kwargs.pop('translate')
                    translate_func = target_field['translate']
                else:
                    translate_func = self.translate
                field_translation = translate_func(field_name, item, **kwargs)
                if (
                    isinstance(field_translation, (list, tuple)) 
                    and len(field_translation)==2 
                    and isinstance(field_translation[0], scrapy.Request)
                    and callable(field_translation[1])
                ):
                    """
                    the translation ends up with a (request, callback_function) tuple or list, 
                    this is an ASYNC transation, let's stop the work for the time being
                    """

                    request, callback = field_translation
                    request.meta['handle_httpstatus_all'] = True
                    request.meta[self.META_KEY] = {
                        'item': new_item,
                        'target_field': field_name,
                        'callback': callback,
                    }
                    return request
                elif isinstance(field_translation, scrapy.Request):
                    logger.warn("translate() returns a Request without callback function, " \
                                "we yield this request but nobody will take care of the translation response")
                    return field_translation
                elif isinstance(field_translation, (str, list, tuple)):
                    new_item[field_name] = field_translation
                else:
                    raise excs.TranslationErrorGeneral(
                        "Translation error, the 'translate()' method returns an unknown type: %s"%str(type(field_translation))
                    )

        # all fields are translated, now it's time to send the item to the engine (and more precesely, the exporter)
        return new_item

    def translate(self, field_name, item, **kwargs):
        raise NotImplementedError
        
    def process_spider_input(self, response, spider):
        if self.META_KEY in response.request.meta:
            if response.status<300:
                raise excs.TranslationResult(response)
            raise excs.TranslationErrorDueToInvalidResponseCode(response)

    def process_spider_exception(self, response, exception, spider):
        if isinstance(exception, excs.TranslationResult):
            """
            Don't be confused, it's not an error. Scrapy only allows us to get the translated result 
            by raising an Exception from process_spider_input()
            """
            callback = response.request.meta[self.META_KEY].get('callback')
            target_field_name = response.request.meta[self.META_KEY]['target_field']
            item = response.request.meta[self.META_KEY]['item']
            target_field = item.fields[target_field_name]
            source_field_name = target_field['source']

            kwargs = target_field.copy()
            kwargs.pop(self.TAG)
            if callback:
                trans_result_callback = callback
            else:
                trans_result_callback = self.get_translate_result
            trans_result = trans_result_callback(response, target_field_name, item, **kwargs)
            item[target_field_name] = trans_result
            return [self.handle_untranslated_item(item)]

        elif isinstance(exception, excs.TranslationError):
            item = response.request.meta[self.META_KEY]['item']
            target_field_name = response.request.meta[self.META_KEY]['target_field']
            target_field = item.fields[target_field_name]
            if target_field.get('on_failure'):
                action = target_field['on_failure']
                if action==FailureAction.RAISE:
                    raise excs.TranslationError
                elif action==FailureAction.DROP_ITEM:
                    return None
                else:
                    if action==FailureAction.REPORT_IN_FIELD:
                        item[target_field_name] = self.IN_FIELD_ERROR_MSG
                    elif action==FailureAction.COPY_SOURCE:
                        source_field_name = target_field['source']
                        source_field_value = item[source_field_name]
                        item[target_field_name] = source_field_value
                    elif action==FailureAction.SET_NULL:
                        item[target_field_name] = None
                    elif action==FailureAction.SET_EMPTY:
                        item[target_field_name] = ''
                    else:
                        raise excs.TranslationErrorGeneral("unknown action: {action}".format(action=action))
                    trans_result = self.handle_untranslated_item(item)
                    return [trans_result]
            else:
                item[target_field_name] = self.IN_FIELD_ERROR_MSG
                trans_result = self.handle_untranslated_item(item)
                return [trans_result]
                    

    def get_translate_result(self, response, field_name, item, **kwargs):
        """
        Default translation callback
        """
        raise excs.TranslationErrorGeneral(
            "Translation response has been recieved but I don't know how to interpret it. " \
            "You need to either specify a callback function in the translate() method or implement "\
            "get_translate_result() method of the middleware"
        )

class LanguageTranslationMiddleware(AutoTranslationMiddlewareBase):

    def get_source_language_code(self, source_field):

        if 'language' in source_field:
            return source_field['language']

        if self.DEFAULT_LANGUAGE is not None:
            return self.DEFAULT_LANGUAGE

        if self.settings.get('DEFAULT_LANGUAGE') is not None:
            return self.settings.get('DEFAULT_LANGUAGE')

        return 'en'

    def translate(self, field_name, item, **kwargs):
        source_field_name = kwargs['source']
        target_field_name = field_name
        source_language = self.get_source_language_code(item.fields[source_field_name])
        target_field = item.fields[target_field_name]
        return self.language_translate(source_language, target_field['language'], item[source_field_name])

    def language_translate(self, source_lang_code, target_lang_code, text):
        raise NotImplementedError

class SyncAutoTranslationMiddleware(LanguageTranslationMiddleware):
    """
    Translate "text" to the language specified by "target_lang_code".
    You need to implement this function only when you choose to go with Synchronous translation.
    Make sure this function is finished real quickly.
    """

    def language_translate(self, source_lang_code, target_lang_code, text):
        return 'Text translated by SyncAutoTranslationMiddleware. If you see this, please rewrite the ' \
               'SyncAutoTranslationMiddleware.translate() method'

class AsyncAutoTranslationMiddleware(LanguageTranslationMiddleware):

    def language_translate(self, source_lang_code, target_lang_code, text):
        return scrapy.Request(
            url = self.get_translate_url( source_lang_code, target_lang_code, text)
        ), self.get_translate_result

    def get_translate_url(self, source_lang_code, target_lang_code, text, **kwargs):
        raise NotImplementedError

    def get_translate_result(self, response, field_name, item, **kwargs):
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
            'https://translation.googleapis.com/language/translate/v2?key={key}' \
            '&q={quoted_text}' \
            '&target={target_lang_code}' \
            '&source={source_lang_code}'.format(
                key=key, 
                quoted_text=quoted_text, 
                target_lang_code=target_lang_code, 
                source_lang_code=source_lang_code
            )

    def get_translate_result(self, response, field_name, item, **kwargs):
        return urlunquote(json.loads(response.text)['data']['translations'][0]['translatedText'])

    def get_api_key(self):
        if hasattr(self, 'api_key') and bool(self.api_key):
            return self.api_key

        key = self.settings.get('GOOGLE_CLOUD_API_KEY')
        if key:
            return key
        raise excs.TranslationErrorGeneral(
            "A Google Cloud API Key must be available. "
            + "You may either add an attribute 'api_key' to the class {cls} or its subclass, ".format(cls=self.__class__.__name__)
            + "add a variable 'GOOGLE_CLOUD_API_KEY' in your settings file, "
            + "or specify it as a command line option like this: "
            + "scrapy crawl <your-spider-name> -s GOOGLE_CLOUD_API_KEY=<your-google-cloud-api-key>"
        )
