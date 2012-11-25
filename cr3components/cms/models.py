from cr3components.cms.middleware import get_current_nolang_path
from cr3components.cms.settings import *
from cr3components.foundation.models import PublishableMixin, SequenceMixin, \
    CurrentSiteInheritanceManager, AdminLinkMixin
from cr3components.multilang.models import *
from cr3components.templateasoption.models import TemplateAsOption
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.query import Q
from django.utils.translation import ugettext_lazy as _
from model_utils.managers import InheritanceManager
from datetime import datetime, date
from mptt.models import MPTTModel
from django.db.utils import IntegrityError
from datetime import date

#TODO: someday add publish_state to all Node components or translations

"""
As per RFC3986

         foo://example.com:8042/over/there?name=ferret#nose
         \_/   \______________/\_________/ \_________/ \__/
          |           |            |            |        |
       scheme     authority       path        query   fragment
          |   _____________________|__
         / \ /                        \
         urn:example:animal:ferret:nose


      path          = path-abempty    ; begins with "/" or is empty
                    / path-absolute   ; begins with "/" but not "//"
                    / path-noscheme   ; begins with a non-colon segment
                    / path-rootless   ; begins with a segment
                    / path-empty      ; zero characters

      path-abempty  = *( "/" segment )
      path-absolute = "/" [ segment-nz *( "/" segment ) ]
      path-noscheme = segment-nz-nc *( "/" segment )
      path-rootless = segment-nz *( "/" segment )
      path-empty    = 0<pchar>


SUM:
wherever we refer to path we mean path-rootless
additionally such path does not contain suffix extension from SEO
path_prefix is a path with trailing slash w/o last element, w/o first slash:
i.e: "over/"
"""



class Category(models.Model):
    slug = models.SlugField(_('slug'))
    name = models.CharField(_('name'), max_length=200)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"
    
class NodeManager(InheritanceManager):
    
    def get_query_set(self):
        return super(NodeManager, self).get_query_set()

    def get_or_create_path(self, path):
#        print self.model
        wayslugs = path.split("/")
        parent = None
        for slug in wayslugs: #just in case, let's create the tree
            #TODO: create full path only if node does not exist
            try:
                node = Node.objects.filter(slug=slug).select_subclasses()[0]
                created = False
            except IndexError:
                node = self.model(slug=slug)
                node.parent = parent
                node.state = 'published'
                node.save()
                node.site.add(Site.objects.get_current())
            parent = node
        return node

    def published(self, now=None):
        if not now:
            now = datetime.now()
        current_site = Site.objects.get_current()
        queryset = self.get_query_set().filter(site=current_site).select_subclasses()
        return queryset.filter(Node.published_q(now))

    def search(self, user, query, language=None):
        queryset = self.published()
        if language:
            queryset = queryset.filter(
                Q(pagecontent__language=language) & (
                    Q(pagecontent__title__icontains=query) | 
                    Q(pagecontent__teaser__icontains=query) | 
                    Q(pagecontent__content__icontains=query)
                )
            )
        else:
            queryset = queryset.filter(
                Q(pagecontent__title__icontains=query) | 
                Q(pagecontent__teaser__icontains=query) | 
                Q(pagecontent__content__icontains=query)
            )
        return queryset


class Node(MPTTModel, PublishableMixin, SequenceMixin, AdminLinkMixin):
    slug = models.SlugField(_('slug'), unique=True)
    template = models.ForeignKey(TemplateAsOption, blank=True, null=True, related_name="node_set")
    child_template = models.ForeignKey(TemplateAsOption, blank=True, null=True, related_name="node_for_child_set")

    is_menu_item = models.BooleanField(_('is menu item'), default=True)
    redirect_to = models.URLField(_('redirect to'), null=True, blank=True)

    parent = models.ForeignKey('self', verbose_name=_('Parent'), null=True, blank=True, related_name="children") #TODO: limit choices to Page
    
    categories = models.ManyToManyField(Category, blank=True)
    
    site = models.ManyToManyField(Site, default=[settings.SITE_ID])
    
    path_prefix_store = models.CharField(max_length=200, null=True, editable=False) #saved path to speed up search
    
    objects = NodeManager()
    on_site = CurrentSiteInheritanceManager()

    def __init__(self, *args, **kwargs):
        super(Node, self).__init__(*args, **kwargs)
        manager = MultiLangManager(object=self)
        self.translate = manager
        self.trans = manager
    
    def __unicode__(self):
        return self.path()
    
    def __iter__(self):
        return iter(self.get_published_children())

    def get_published_children_in_menu(self):
        all = self.get_children().filter(is_menu_item=True).filter(self.published_q())
        return all

    def get_published_children(self):
        return self.get_children().filter(self.published_q()).select_subclasses()
    
    def get_children(self):
        return Node.objects.filter(parent=self).select_subclasses()
        
    def get_template(self):
        """
        returns template to render Node page
        if necessary traverses through parents
        """
        if self.template:
            return self.template
        elif self.parent:
            return self.parent.get_child_template()
        else:
            return CMS_TEMPLATE

    def get_child_template(self):
        if self.child_template:
            return self.child_template
        elif self.template:
            return self.template
        else:
            if self.parent:
                return self.parent.get_child_template()
            else:
                return CMS_TEMPLATE

    def path(self):
        return "%s%s" % (self.path_prefix(), self.slug)
    
    def path_prefix(self):
        return "".join(map(lambda x: "%s/" % x.slug, self.get_ancestors()))

    @models.permalink
    def get_absolute_url(self):
        return ('node', [self.path()])
    
    def save(self, *args, **kwargs):
        super(Node, self).save(*args, **kwargs) #workaround for mptt limitation
        try:
            self.path_prefix_store = self.path_prefix()
        except NotImplementedError:
            pass
        super(Node, self).save(*args, **kwargs)

    class MultiLangMeta:
        translated_language_field = "language"
        translated_queryset = "nodecontent_set"
        translated_fields = ["title", 'menu_entry', 'teaser', 'content'] #later take list of fielrs from related model
        filter_querysets = ["nodeimage_set"]
    
    class SearchMeta:
        fields = ["nodecontent__title", "nodecontent__teaser", "nodecontent__content", "nodeimage__title", "nodeattachment__title"]
        filter_func = PublishableMixin.published_q
        template = "cms/inc_node_search.html"
    
    class Meta:
        unique_together = ("slug", "parent")

    class MPTTMeta:
        order_insertion_by = ['sequence', 'slug']

class PageNode(Node):
    objects = NodeManager()
    on_site = CurrentSiteInheritanceManager()

    

    class Meta:
        ordering = ('slug',)


class PostNode(Node):
    objects = NodeManager()
    on_site = CurrentSiteInheritanceManager()

    
    def path_prefix(self):
        """
        date in url for post node that has not been published will change
        """
        if self.published_on:
            return self.published_on.strftime("%Y/%m/%d/")
        else:
            return date.today().strftime("%Y/%m/%d/")

    class Meta:
        ordering = ('-created_on',)

class FilterNode(Node):
    """
    Model that returns filtered posts instead of sub nodes
    """
    filter_category = models.ForeignKey(Category)

    objects = NodeManager()
    on_site = CurrentSiteInheritanceManager()

    def get_children(self):
        return Node.objects.filter(categories=self.filter_category).filter(self.published_q()).select_subclasses() #TODO:test it
    
    class Meta:
        ordering = ('-created_on',)

class NodeContent(models.Model):
    node = models.ForeignKey(Node)
    language = models.CharField(max_length=2, choices=LANGUAGES, default=LANGUAGE_CODE[:2])

    title = models.CharField(_('title'), max_length=200)
    menu_entry = models.CharField(_('menu entry'), max_length=200, blank=True)

    meta_title = models.CharField(_('meta title'), max_length=250, null=True, blank=True)
    meta_keywords = models.CharField(_('meta keywords'), max_length=250, null=True, blank=True)
    meta_description = models.CharField(_('meta description'), max_length=1000, null=True, blank=True)

    teaser = models.TextField(_('teaser'), null=True, blank=True)
    content = models.TextField(_('content'), null=True, blank=True)

    def __unicode__(self):
        return "%s:%s" % (self.title, self.language)

    def save(self):
        if not self.menu_entry:
            self.menu_entry = self.title

        super(NodeContent, self).save()

class NodeImage(models.Model):
    node = models.ForeignKey(Node)
    language = models.CharField(max_length=2, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE[:2])

    title = models.CharField(_('title'), max_length=200)
    file = models.ImageField(upload_to='images', help_text=_("Image to attach"))
    alt = models.CharField(_("Alternative text"), max_length=100, blank=True, help_text=_("Alternative text for blind users shown also in popup"))

    sequence = models.IntegerField(default=100)

class NodeAttachment(models.Model):
    node = models.ForeignKey(Node)
    language = models.CharField(max_length=2, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE[:2])

    title = models.CharField(_('title'), max_length=200, blank=True)
    file = models.FileField(upload_to='attachements', help_text=_("File to attach"))
    alt = models.CharField(_("Alternative text"), max_length=100, blank=True, help_text=_("Alternative text for blind users shown also in popup"))

    sequence = models.IntegerField(default=100)



class TargetNodesSite(models.Model):
    site = models.ForeignKey(Site)
    node = models.ForeignKey(Node)
    on_site = CurrentSiteManager()
    
    def __unicode__(self):
        return u'%s' % self.node

#from manggha import search
#search.site.register(Node)


class CmsSite(models.Model):
    site = models.OneToOneField(Site)
    google_analytics_id = models.CharField(_('Google Analytics ID'), max_length=200)
    site_title = models.CharField(_('Site title'), max_length=200)
    on_site = CurrentSiteManager()

