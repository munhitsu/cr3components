from django.conf import settings
from cr3components.multilang.settings import *



CMS_ROOT = getattr(settings,"CMS_ROOT","/")
CMS_TEMPLATES = getattr(settings, "CMS_TEMPLATES", (('cms/base_node.html', 'cms/base_node.html'),))
CMS_TEMPLATE = getattr(settings,"CMS_TEMPLATE",'cms/base_node.html')
CMS_DEFAULT_PUBLISHED = getattr(settings,"CMS_DEFAULT_PUBLISHED",True)
CMS_DEFAULT_MENU_ITEMS_LIMIT = getattr(settings,"CMS_DEFAULT_MENU_ITEMS_LIMIT",-1)
