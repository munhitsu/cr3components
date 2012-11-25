from django.conf.urls.defaults import *
from django.views.generic import TemplateView
from django.conf import settings

from cr3components.cms.views import *

from cr3components.cms.feeds import LatestPostNodesFeed

#CR3CMS_PAGE_SUFFIX

SUFFIX = settings.CR3CMS_PAGE_SUFFIX.replace(".","\.")

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="cms/base_root.html"), name="node_root"),
    url(r'^(?P<path>(?P<path_prefix>([-\w]+/))*(?P<slug>[-\w]+))/print$', node_print_view, name="node_print"),
    url(r'^(?P<path>(?P<path_prefix>([-\w]+/))*(?P<slug>[-\w]+))%s$' % SUFFIX, node_view, name="node"),
    url(r'^rss/$', LatestPostNodesFeed()),
)
