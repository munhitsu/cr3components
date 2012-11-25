from django.db import models
from django.contrib.contenttypes.models import ContentType





# Create your models here.
class TemplateAsOption(models.Model):
    path = models.CharField(max_length=255)
    type = models.ForeignKey(ContentType)
    sequence = models.PositiveIntegerField(default=100)
    is_default = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['sequence']
    
    def __unicode__(self):
        return self.path

#TODO: add validation that template exist (on save)
#TODO: add dedicated field (ForeignKey wrapper that uses is_default and content type to limit choice)
#TODO: add validation only one default per type
