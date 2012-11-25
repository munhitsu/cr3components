from cr3components.templateasoption.models import TemplateAsOption
from django.contrib import admin



class TemplateAsOptionAdmin(admin.ModelAdmin):
    list_display = ('path', 'type','sequence','is_default')
    list_editable = ('sequence',)   

admin.site.register(TemplateAsOption, TemplateAsOptionAdmin)
