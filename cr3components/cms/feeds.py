from django.contrib.syndication.views import FeedDoesNotExist, Feed
from django.shortcuts import get_object_or_404
from django.contrib.sites.models import Site
from cr3components.cms.models import PostNode


#TODO: how to make it lang dependent?

class LatestPostNodesFeed(Feed):
    description_template = 'cms/feeds/post_description.html'

    def items(self):
        return PostNode.objects.published().order_by('-pub_date')

#TODO: add category feed
