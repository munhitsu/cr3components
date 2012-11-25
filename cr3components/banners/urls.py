from cr3components.banners.views import redirect
from django.conf.urls.defaults import *

#fiction

urlpatterns = patterns('',
    url(r'^redirect/$',
    redirect,
    name="banner_redirect"),
)
