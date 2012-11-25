# @copyright cr3studio.com
# @author cr3studio.com
# @link http://cr3studio.com/

from django.dispatch import dispatcher
from django.contrib.auth import models as auth_app
from django.db.models.signals import post_syncdb
from django.dispatch import receiver
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist

from cr3components.cms import models as cms_app


@receiver(post_syncdb, sender=auth_app)
def setup_users(app, created_models, verbosity, **kwargs):
    print "Preloading Users."
    if auth_app.User.objects.count() > 0:
        print " skipped"
    else:
        username = 'admin'
        email = 'admin@cr3studio.com'
        password = 'admin'
        auth_app.User.objects.create_superuser(username, email, password)
        print "Superuser (admin) created successfully."


@receiver(post_syncdb, sender=cms_app)
def create_cmssite(app, created_models, verbosity, **kwargs):
    try:
        cmssite = Site.objects.get_current().cmssite
    except ObjectDoesNotExist:
        print "Creating initial CmsSite object"
        create_defaut_cmssite()

def create_defaut_cmssite():
    site = Site.objects.get_current()
    cmssite = cms_app.CmsSite(site=site,google_analytics_id="N/A",site_title="TBD")
    cmssite.save()
    return cmssite
