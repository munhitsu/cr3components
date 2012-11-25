from cr3components.foundation.models import PublishableMixin, SequenceMixin
from cr3components.foundation.named import named
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.query import Q
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from model_utils.managers import InheritanceManager

from django.conf import settings

class BannerRoll(PublishableMixin):
    slug = models.SlugField()

    def banners(self):
        """
        Helper function that returns QuerySet that is :
        - published
        - ordered
        - select_subclasses
        """
        return self.banner_set.filter(self.published_q()).order_by("sequence").select_subclasses()
    banners = property(banners)
    
    def render(self, context=None, template="banners/inc_banner_roll.html"):
        """
        Render only if published
        """
        if self.published():
            return render_to_string(template, {"banner_roll":self}, context)
        else:
            if settings.DEBUG:
                return "banner(%s) is not published" % self.slug
            else:
                return ""

    def __unicode__(self):
        return self.slug


class Banner(PublishableMixin, SequenceMixin):
    banner_roll = models.ForeignKey(BannerRoll)
    redirect_to = models.URLField(_('redirect to'), null=True, blank=True)

    objects = InheritanceManager();
    
    def render(self, context=None, template=None):
        raise Exception("Override me")

class BannerImage(Banner):
    image = models.ImageField(upload_to='banners')
    alt = models.CharField(max_length=128, blank=True)

    objects = InheritanceManager();

    def render(self, context=None, template="banners/inc_banner_image.html"):
        return render_to_string(template, {"banner":self}, context)


class BannerFlash(Banner):
    flash = models.FileField(upload_to='banners',blank=False)
    width = models.PositiveIntegerField(blank=False)
    height = models.PositiveIntegerField(blank=False)
    flash_ver = models.PositiveSmallIntegerField(blank=False)
    bgcolor = models.CharField(max_length=7,default="#FFFFFF")

    objects = InheritanceManager();
    
    def render(self, context=None, template="banners/inc_banner_flash.html"):
        return render_to_string(template, {"banner":self}, context)


