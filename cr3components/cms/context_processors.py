from cr3components.cms.models import *
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist



def request_is_secure(request):
    if request.is_secure():
        return True
    if 'HTTP_X_FORWARDED_SSL' in request.META:
        return request.META['HTTP_X_FORWARDED_SSL'] == 'on'
    return False

def cms(request):
    is_secure = request_is_secure(request)
    root_nodes = Node.objects.published().filter(parent__isnull=True) #We're not depending on tree as tree is not aware of inheritance

    try:
        site_title = Site.objects.get_current().cmssite.site_title
    except ObjectDoesNotExist:
        print "WARNING: Create Site.cmsSite object"
        site_title = None

    if is_secure:
        try:
            media_url = settings.MEDIA_SECURE_URL
        except AttributeError:
            media_url = settings.MEDIA_URL.replace('http://','https://')
    else:
        media_url = settings.MEDIA_URL
    return {
        'media_url': media_url,
        'is_secure' : is_secure,
#        'request' : request,
        'session' : request.session,
        'site_title' : site_title,
        'domain': Site.objects.get_current().domain,
        'root_nodes': root_nodes,
    }
