from model_utils.managers import InheritanceManager
from django.conf import settings
from django.db import models
from datetime import datetime


class CurrentSiteInheritanceManager(InheritanceManager):

    def get_query_set(self):
        #if one knows how to make it prettier...
        return super(CurrentSiteInheritanceManager, self).get_query_set().filter(site__id__exact=settings.SITE_ID)



class PublishableManager(models.Manager):
    use_for_related_fields = True

    def published(self, now=None):
        if not now:
            now = datetime.now()
        return self.get_query_set().filter(self.model.published_q(now))


#TODO:
#create query set that exposes easily:
# - current_site
# - published
# - inheritance cast
