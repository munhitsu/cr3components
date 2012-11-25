from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.contrib import admin
from cr3components.cms import NodeSitemap
admin.autodiscover()

handler500 # Pyflakes

#from cr3components.cms import NodeSitemap

sitemaps = {
    'nodes': NodeSitemap,
}


urlpatterns = patterns(
    '',
#    (r'^admin/templatesadmin/', include('templatesadmin.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )

urlpatterns += staticfiles_urlpatterns()

urlpatterns += patterns('',
    url(r'^markitup/', include('markitup.urls')),
    (r'^', include('cr3components.cms.urls')),
)



