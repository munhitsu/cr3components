from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from django import forms
from django.utils.safestring import mark_safe
from django.contrib.sites.admin import SiteAdmin
from django.contrib.sites.models import Site
 
 
class AdminThumbWidget(AdminFileWidget):
    """
    Widget that displays image thumbnail
    FIXME: does not work in Inline
    """
    def render(self, name, value, attrs=None):
        output = []
        output.append('<a target="_blank" href="%s"><img src="%s"/></a><br />' % \
            (value.admin.url, value.admin.url))

        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))



def extend_admin_site_inlines(inline_class,admin_site=admin.site):
    """
    Extends admin for Site class with specific inline class
    1. Create model referring to Site class (configuration nature)
    2. Create admin inline class for this model
    3. Extend SiteAdmin class with your inline model
    """
    extend_class_inlines(inline_class,SiteAdmin,Site,admin_site=admin.site)


def extend_class_inlines(inline_class,admin_class,model_class,admin_site):
    """
    """
    
    for registered_model in admin_site._registry:
        registered_admin = admin_site._registry[registered_model]
        
        if isinstance(registered_admin,admin_class):
#            print "Extending"
#            print " admin class %s" % registered_admin
#            print " for model %s" % registered_model
            inline_instance = inline_class(model_class, admin_site)
            registered_admin.inline_instances.append(inline_instance)
#            registered_admin.inlines.append(inline_class) #breaks admin athough seems to be logical step there
