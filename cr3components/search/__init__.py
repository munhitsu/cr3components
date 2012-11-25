from django.db.models.query import Q
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from foundation.named import named

#register a model that has a banager having method
# search(self, user, query, language=None):
# method shall return Q object

#distinct is executed once at the end

class ModelIsNotSearchable(Exception):
    pass

class SearchManager():
    registered_models = []
    query = None

    def __init__(self):
        if not hasattr(settings, "SEARCHABLE_MODELS"):
            print 'Remember to define "settings.SEARCHABLE_MODELS"'
        
        for x in settings.SEARCHABLE_MODELS:
            self._register(named(x))
 
    def _register(self,model):
        if not hasattr(model,"SearchMeta"):
            raise ModelIsNotSearchable, unicode(_('Please define class SearchMeta'))
        meta_attr = getattr(model,"SearchMeta")

        if not hasattr(meta_attr,"fields"):
            raise ModelIsNotSearchable, unicode(_('Please define SearchMeta.fields = []'))

        if not hasattr(meta_attr,"template"):
            raise ModelIsNotSearchable, unicode(_('Please define SearchMeta.template = ""'))

        self.registered_models.append(model)


    def _get_keywords(self,keywords_string):
        #TODO: remove punctuation and common words
        return filter(lambda x: x, keywords_string.split(" "))        

    def _get_q4tuple(self,field,value):
        h = { field: value }
        return Q(**h)

    def _get_q4model(self,model,keywords):
        if not hasattr(model,"SearchMeta"):
            raise ModelIsNotSearchable, unicode(_('Please define class SearchMeta'))
        meta_attr = getattr(model,"SearchMeta")

        if not hasattr(meta_attr,"fields"):
            raise ModelIsNotSearchable, unicode(_('Please define SearchMeta.fields = []'))
        fields = getattr(meta_attr,"fields")

        keyword_qs = []
        for keyword in keywords:
            qdict = dict()
            qlist = []
            field_qs = map(lambda field: self._get_q4tuple(field+"__icontains",keyword), fields)
            keyword_q = reduce(lambda x,y: x | y, field_qs)
            keyword_qs.append(keyword_q)

        qfin = reduce(lambda x,y: x & y, keyword_qs)
        if hasattr(meta_attr,"filter_func"):
            fq = getattr(meta_attr,"filter_func")()
            qfin = qfin & fq
        return Q(qfin)
    
    def _objects4model(self,model,keywords):
        return model.objects.filter(self._get_q4model(model,keywords))
    
    def _objects(self,keywords_string):
        keywords = self._get_keywords(keywords_string)
        if keywords:
            os = map(lambda model: self._objects4model(model, keywords), self.registered_models)
            oses = reduce(lambda x: x|x,os)
            return oses
        else:
            return None
    
    def objects(self):
        if self.query:
            return self._objects(self.query)
        else:
            return None

manager = SearchManager()
