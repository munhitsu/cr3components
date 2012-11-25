from django.core.cache import cache

def cacheable(cache_key, timeout=3600):
    """
    a nice method decorator
    http://www.djangosnippets.org/snippets/1130/
    # fields [id, name etc]
    @cacheable("SomeClass_get_some_result_%(id)s")
    def get_some_result(self):
    """
    def paramed_decorator(func):
        def decorated(self):
            key = cache_key % self.__dict__
            res = cache.get(key)
            if res == None:
                res = func(self)
                cache.set(key, res, timeout)
            return res
        decorated.__doc__ = func.__doc__
        decorated.__dict__ = func.__dict__
        return decorated 
    return paramed_decorator
