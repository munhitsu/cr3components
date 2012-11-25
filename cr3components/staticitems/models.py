# @copyright cr3studio.com
# @author cr3studio.com
# @link http://cr3studio.com/

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet

class SubclassingQuerySet(QuerySet):
    def __getitem__(self, k):
        result = super(SubclassingQuerySet, self).__getitem__(k)
        if isinstance(result, models.Model) :
            return result.as_leaf_class()
        else :
            return result

class StaticItemManager(models.Manager):
    def get_query_set(self):
        return SubclassingQuerySet(self.model)

class StaticItem(models.Model):
    slug = models.SlugField(_("slug name"), unique=True)
    order = models.IntegerField(default=100)
    template = "staticitems/inc_basic.html"

    content_type = models.ForeignKey(ContentType,editable=False,null=True)

    objects = StaticItemManager()
    
    def save(self):
        if(not self.content_type):
            self.content_type = ContentType.objects.get_for_model(self.__class__)
        self.save_base()

    def as_leaf_class(self):
        content_type = self.content_type
        model = content_type.model_class()
        return model.objects.get(id=self.id)

    def __unicode__(self):
        item = self.as_leaf_class()
        if item == self:
            return self.slug
        else:
            return item.__unicode__()

    def _render(self, context=None, template=None):
        if not template:
            template = self.template
        return render_to_string(template, {"static_item":self}, context)

    def render(self, context=None, template=None):
        item = self.as_leaf_class()
        return item._render(context,template)


class Image(StaticItem):
    image = models.ImageField(_("image"), upload_to='staticitems')
    alt = models.CharField(_("alternative text"), max_length=100, blank=True)
    template = "staticitems/inc_image.html"

    def get_absolute_url(self):
        return self.file.url
    
    def __unicode__(self):
        return str(self.slug)+": "+str(self.image)

    class Meta:
        ordering = ['order','slug']
        verbose_name = _('Image')
        verbose_name_plural = _('Images')


class File(StaticItem):
    file = models.FileField(_("file"), upload_to='staticitems')
    alt = models.CharField(_("alternative text"), max_length=100, blank=True)
    template = "staticitems/inc_file.html"
    
    def get_absolute_url(self):
        return self.file.url

    def __unicode__(self):
        return str(self.slug)+": "+str(self.file)

    class Meta:
        ordering = ['order','slug']
        verbose_name = _('File')
        verbose_name_plural = _('Files')

class Flash(StaticItem):
    flash = models.FileField(upload_to='banners',blank=False)
    width = models.PositiveIntegerField(blank=False)
    height = models.PositiveIntegerField(blank=False)
    flash_ver = models.PositiveSmallIntegerField(blank=False)
    bgcolor = models.CharField(max_length=7,default="#FFFFFF")
    template = "staticitems/inc_flash.html"

    def get_absolute_url(self):
        return self.flash.url
    
    def __unicode__(self):
        return str(self.slug)+": "+str(self.flash)

    class Meta:
        ordering = ['order','slug']
        verbose_name = _('Flash')
        verbose_name_plural = _('Flashes')

class Snippet(StaticItem):
    text = models.TextField(_('text'), null=True, blank=True)
    template = "staticitems/inc_snippet.html"

    def __unicode__(self):
        return str(self.slug)

    class Meta:
        ordering = ['order','slug']
        verbose_name = _('Snippet')
        verbose_name_plural = _('Snippets')
