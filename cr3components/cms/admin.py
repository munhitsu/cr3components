from cr3components.cms.forms import *
from cr3components.cms.models import *
from cr3components.foundation.admin import extend_admin_site_inlines, \
    AdminThumbWidget
from django import forms, template
from django.contrib import admin
from django.contrib.admin import helpers
from django.core.context_processors import csrf
from django.forms.models import BaseInlineFormSet
from django.shortcuts import render_to_response
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext as _
from markitup.widgets import MarkItUpWidget
from mptt.admin import MPTTModelAdmin
from mptt.exceptions import InvalidMove





class NodeImageInlineAdmin(admin.TabularInline):
    model = NodeImage
    extra = 0

#    formfield_overrides = {
#        models.ImageField: {'widget': AdminThumbWidget},
#    }

class NodeAttachmentInlineAdmin(admin.TabularInline):
    model = NodeAttachment
    extra = 0


class NodeContentInlineAdmin(admin.StackedInline):
    model = NodeContent
    inlines = [NodeImageInlineAdmin, NodeAttachmentInlineAdmin,]
    extra = 0
    fieldsets = (
        (None, {
            'fields': ('language','title','menu_entry','teaser','content')
        }),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': ('meta_title','meta_keywords','meta_description')
        }),
    )
    formfield_overrides = {
        models.TextField: {'widget': MarkItUpWidget},
    }

class NodeChildOrderInline(BaseInlineFormSet): 
    extra = 0
    def __init__(self, *args, **kwargs): 
        super(NodeChildOrderInline, self).__init__(*args, **kwargs) 
        self.can_delete = False 


class NodeChildOrderInlineAdmin(admin.TabularInline):
    model = Node
    extra = 0
    verbose_name = "Child order"
    verbose_name_plural = "Children order"
    formset = NodeChildOrderInline
    fields = ['sequence','is_menu_item']



class ConfigTargetNodeForm(forms.Form):
    config_node = forms.ModelChoiceField(queryset=TargetNodesSite.on_site, empty_label=None, label="Target Node")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name')

class NodeAdmin(MPTTModelAdmin):
    form = NodeAdminForm
    actions = ['move_to']
    list_display = ('slug', 'path', 'published', 'is_menu_item')
    list_filter = ('state','parent')
    search_fields = ('slug',"nodecontent__title","nodecontent__teaser","nodecontent__content","nodeimage__title","nodeattachment__title")
    inlines = [NodeContentInlineAdmin,NodeImageInlineAdmin,NodeAttachmentInlineAdmin,NodeChildOrderInlineAdmin]
    fieldsets = (
        (None, {
            'fields': ('slug','parent','categories','state')
        }),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': ('site','start_publish_date','end_publish_date','template','child_template','is_menu_item','sequence','redirect_to')
        }),
    )
    
    def move_to(self,request, queryset):
        if request.POST.get('post'):
            form = ConfigTargetNodeForm(request.POST)
            if form.is_valid():
                config_node = form.cleaned_data['config_node']
                n = queryset.count()
                if n:
                    for node in queryset.all():
                        try:
                            node.parent = config_node.node
                            node.save()
                            self.message_user(request, _("Successfully moved %(node)s to %(target_node)s.") % {
                                "node": node,
                                "target_node": config_node.node
                            })
                        except InvalidMove as inst:
                            self.message_user(request, ("ERROR moving %(node)s: %(error)s") % {
                                "node" : node.slug,
                                "error" : inst,
                            })
                # Return None to display the change list page again.
                return None
            else:
                messages.error(request, _("ERROR: Please select existing node!"))
        else:
            opts = self.model._meta
            app_label = opts.app_label

            form = ConfigTargetNodeForm()
            c = {
                "title": _("Select Target Node"),
                "object_name": force_unicode(opts.verbose_name),
                'queryset': queryset,
                "opts": opts,
                "root_path": self.admin_site.root_path,
                "app_label": app_label,
                'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
                'form': form
            }
            c.update(csrf(request))
            return render_to_response("admin/cms/node/move_to.html", c, context_instance=template.RequestContext(request))

    class Media:
        js = ("http://www.google.com/jsapi","/static/js/cms/jqjqui_load.js",
              "/static/js/cms/admin/inline_tab_sort.js",
              )

class FilterNodeAdmin(NodeAdmin):
    fieldsets = (
        (None, {
            'fields': ('slug','parent','filter_category','state')
        }),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': ('site','start_publish_date','end_publish_date','template','child_template','is_menu_item','sequence','redirect_to')
        }),
    )
    

class CmsSiteInline(admin.StackedInline):
    model = CmsSite

class TargetNodesSiteInline(admin.TabularInline):
    model = TargetNodesSite
    extra = 0

extend_admin_site_inlines(CmsSiteInline)
extend_admin_site_inlines(TargetNodesSiteInline)

admin.site.register(Category, CategoryAdmin)
admin.site.register(PageNode, NodeAdmin)
admin.site.register(PostNode, NodeAdmin)
admin.site.register(FilterNode, FilterNodeAdmin)
