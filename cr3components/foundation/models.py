from datetime import datetime
from django.contrib.sites.managers import CurrentSiteManager
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django_fsm.db.fields import FSMField, transition
from pandora import box
from django.conf import settings

from cr3components.foundation.managers import CurrentSiteInheritanceManager

    

class PublishableMixin(models.Model):
    """
    Initial state is draft. To override available states add/remove @transitions.
    """

    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_on = models.DateTimeField(auto_now=True, null=True, blank=True)
    published_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    state = FSMField(_("Item state"), default='draft')
    start_publish_date = models.DateTimeField(_('start publishing'), null=True, blank=True)
    end_publish_date = models.DateTimeField(_('finish publishing'), null=True, blank=True)


    @transition(source=('draft', 'on_hold'), target='published', save=True)
    def publish(self):
        self.published_on = datetime.now()

    @transition(source=('draft', 'published'), target='on_hold', save=True)
    def hold(self):
        pass


    def published(self, now=None):
        if not now:
            now = datetime.now()
        if self.state == 'published' \
            and (not self.start_publish_date or self.start_publish_date <= now) \
            and (not self.end_publish_date or self.end_publish_date >= now):
            return True
        else:
            return False
    published.boolean = True
    published.short_description = _("Visible")

    def published_q(self, now=None):
        if not now:
            now = datetime.now()
        return Q(Q(state='published'),
            Q(start_publish_date__lte=now) | Q(start_publish_date__isnull=True),
            Q(end_publish_date__gte=now) | Q(end_publish_date__isnull=True)
            )
    published_q = classmethod(published_q)


    class Meta:
        abstract = True
        ordering = ('-created_on',)

class SequenceMixin(models.Model):
    sequence = models.IntegerField(default=100)

    class Meta:
        abstract = True
        ordering = ('sequence',)



class AdminLinkMixin(object):

    def admin_edit_link(self):
        if self.pk:
            return reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.module_name), args=[self.pk])            
        else:
            return None

    def admin_edit_inline(self):
        #TODO: change into template render
        user = box['user']
        if user and user.is_staff and (user.is_superuser or user.has_perm('%s.can_edit' % self._meta.app_label, self)):
            return mark_safe(u'<a href="%s">edit</a>' % self.admin_edit_link())
        else:
            return ""
