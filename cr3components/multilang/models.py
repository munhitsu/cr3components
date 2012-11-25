from django.utils import translation
from django.conf import settings


LANGUAGES_FALLBACK = getattr(settings,"LANGUAGES_FALLBACK",dict())

class MultiLangManager():
    """
    optimized for small amount of languages but lots of fallbacks
    has to be created from __init__ as requires object instance
    """
    _object = None
    _model = None
    _lang = None
    _qs = None
    _all = None
    _meta = None
    _querysets_all = dict()
    _late_init_done = False

    def __init__(self, object):
        self._object = object
        self._model = object.__class__
        self._lang = translation.get_language()[:2]

    def _late_init(self): #late init is forced by InheritanceManager
        object = self._object
        self._qs = getattr(object,object.MultiLangMeta.translated_queryset)
        self._all = self._qs.all()
        self._meta = object.MultiLangMeta
        for qs_name in self._object.MultiLangMeta.filter_querysets:
            self._querysets_all[qs_name] = getattr(self._object,qs_name).all()
        self._late_init_done = True

    def _get_translation_object_fallback(self,lang):
        o = None
        while lang and not o:
            o = self._get_translation_object(lang)
            if LANGUAGES_FALLBACK.has_key(lang):
                lang = LANGUAGES_FALLBACK[lang]
            else:
                lang = None
        return o

    def _get_translation_object(self,lang):
        for o in self._all:
            if getattr(o,self._object.MultiLangMeta.translated_language_field) == lang:
                return o
        return None

    def _get_queryset_objects_fallback(self,lang,filter_queryset):
        os = None
        while lang and not os:
            os = self._get_queryset_objects(lang,filter_queryset)
            if LANGUAGES_FALLBACK.has_key(lang):
                lang = LANGUAGES_FALLBACK[lang]
            else:
                lang = None
        return os

    def _get_queryset_objects(self,lang,filter_queryset):
        os = []
        for o in self._querysets_all[filter_queryset]:
            if getattr(o,self._object.MultiLangMeta.translated_language_field) == lang:
                os.append(o)
        return os

    def __getattr__(self, attr):
        if not self._late_init_done:
            self._late_init()
        if attr in self._object.MultiLangMeta.translated_fields:
            to = self._get_translation_object_fallback(self._lang)
            if to:
                return getattr(to,attr)
            elif hasattr(self._object,attr):
                return getattr(self._object,attr)
            else:
                return None #or "" - to consider
        elif attr in self._object.MultiLangMeta.filter_querysets:
            return self._get_queryset_objects_fallback(self._lang,attr)
#            return getattr(self._object,attr).all().extra(where=["language == '%s'" % self._lang])
        else:
            raise AttributeError, attr  # <<< DON'T FORGET THIS LINE !!
