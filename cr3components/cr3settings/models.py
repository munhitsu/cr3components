from django.db import models
from django.conf import settings
# Create your models here.


CR3SETTINGS = getattr(settings, "CR3SETTINGS", {})

class CR3Settings (models.Model):
    key = models.CharField(max_length=255, primary_key=True)
    value = models.TextField(null=True)

    @staticmethod
    def get(key, default=None):
        """
        Returns from storage.
        If storage does dot have the key than fallbacks to settings and creates key->value pair.
        In case there was no setting in settings than default value is used and stored.
        """
        try:
            kv = CR3Settings.objects.get(key=key)
            return kv.value
        except CR3Settings.DoesNotExist:
            settings_value = settings.CR3SETTINGS.get(key)
            if settings_value is None:
                settings_value = default
            kv = CR3Settings.objects.create(key=key, value=settings_value)
            return settings_value

    def revert_to_default(self):
        """
        imports value from settings.CR3SETTINGS
        if key is not available in settings than storage is deleted
        returns true if elemend has been updated
        """
        if not settings.CR3SETTINGS.has_key(self.key):
            self.delete()
            return True
        settings_value = settings.CR3SETTINGS.get(self.key)
        if self.value != settings_value:
            self.value = settings_value
            self.save()
            return True
        return False

    class Meta:
        verbose_name = "CR3Settings"
        verbose_name_plural = "CR3Settings"
