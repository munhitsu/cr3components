from django.utils import translation
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect

class HttpResponseRedirectMultiLang(HttpResponseRedirect):
    def __init__(self, redirect_to):
        #TODO: someday extend to language switching via extra argument
        if len(redirect_to) > 0 and redirect_to[0] == "/":
            lang = translation.get_language()
            path = "/%s%s" % (lang, redirect_to)
        else:
            path = redirect_to
        HttpResponseRedirect.__init__(self, path)

class HttpResponsePermanentRedirectMultiLang(HttpResponsePermanentRedirect):
    def __init__(self, redirect_to):
        #TODO: someday extend to language switching via extra argument
        if len(redirect_to) > 0 and redirect_to[0] == "/":
            lang = translation.get_language()
            path = "/%s%s" % (lang, redirect_to)
        else:
            path = redirect_to
        HttpResponsePermanentRedirect.__init__(self, path)
