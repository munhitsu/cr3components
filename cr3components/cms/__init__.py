from django.contrib.sitemaps import Sitemap
from cr3components.cms.models import Node


#TODO no published atribute taken into consideration

class NodeSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Node.objects.published()

    def lastmod(self, obj):
        return obj.modified_on
