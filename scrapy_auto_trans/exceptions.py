from scrapy.exceptions import IgnoreRequest

class TranslationResult(IgnoreRequest):
    """A translation response was received"""

    def __init__(self, response, *args, **kwargs):
        self.response = response
        super(TranslationResult, self).__init__(*args, **kwargs)

class TranslationError(Exception):
    def __init__(self):
        pass

    def error(self):
        return "Translation Error"

    def warn(self):
        return self.error()

    def details(self):
        return self.error()

class TranslationErrorGeneral(TranslationError):

    def __init__(self, message):
        self.message = message
        super(TranslationErrorGeneral, self).__init__()

    def warn(self):
        return self.message

class TranslationErrorDueToInvalidResponseCode(TranslationError):
    def __init__(self, response):
        self.response = response
        super(TranslationErrorDueToInvalidResponseCode, self).__init__()

    def warn(self):
        return "translation failed due to response code = %d"%self.response.status

    def details(self):
        return "translation failed due to response code = %d, request url = '%s'"%(
            self.response.status,
            self.response.request.url
        )
    
