# threadlocals middleware
try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

_thread_locals = local()
def get_current_user():
    return getattr(_thread_locals, 'user', None)

def get_current_path():
    return getattr(_thread_locals, 'path', None)

def get_current_nolang_path():
    return getattr(_thread_locals, 'nolang_path', None)

class CmsMiddleware(object):
    """Middleware that gets various objects from the
    request object and saves them in thread local storage."""
    def process_request(self, request):
        _thread_locals.user = getattr(request, 'user', None)
        _thread_locals.path = getattr(request, 'path', None)
        _thread_locals.nolang_path = getattr(request, 'nolang_path', None)
