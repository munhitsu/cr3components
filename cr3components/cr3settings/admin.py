from django.contrib import admin
from cr3components.cr3settings.models import CR3Settings
from django.utils.translation import ugettext as _


class CR3SettingsAdmin(admin.ModelAdmin):
    list_display = ('key', 'value')
    search_fields = ('key', 'value')
    actions = ['revert_to_default']

    def revert_to_default(self, request, queryset):
        n = queryset.count()
        if n:
            for node in queryset.all():
                key = node.key
                updated = node.revert_to_default()
                if updated:
                    self.message_user(request, _("Successfully updated: %(key)s") % {
                        "key": key,
                    })
                else:
                    self.message_user(request, _("Ignored: %(key)s") % {
                        "key": key,
                    })
        return None


admin.site.register(CR3Settings, CR3SettingsAdmin)
