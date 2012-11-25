from django.conf import settings
from django.conf import global_settings
from django import http
from django.middleware.common import _is_valid_path
from django.utils import translation

def is_supported_lang(lang):
    for lt in settings.LANGUAGES:
        if lt[0] == lang:
            return True
    return False

def is_lang(lang):
    for lt in global_settings.LANGUAGES:
        if lt[0] == lang:
            return True
    return False    

class MultiLangMiddleware(object):
    def process_request(self, request):
        path = request.path
        lang_token = path.split("/")[1]
        nolang_path = request.path[len(lang_token)+1:]
        if is_lang(lang_token):
            request.nolang_path = nolang_path
            if is_supported_lang(lang_token):
                translation.activate(lang_token)
                request.LANGUAGE_CODE = translation.get_language()
                if lang_token == settings.LANGUAGE_CODE:
                    return http.HttpResponsePermanentRedirect(nolang_path)
            else:
                return http.HttpResponseNotFound("Language %s is not available" % lang_token)
        else:
            #TODO: consider checking browser language here
            request.nolang_path = request.path
            translation.activate(settings.LANGUAGE_CODE)
            request.LANGUAGE_CODE = translation.get_language()
            return None #not a language so it's ok
