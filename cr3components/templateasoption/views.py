# Create your views here.
from django.views.generic.detail import SingleObjectTemplateResponseMixin

class TemplateAsOptionMixin(SingleObjectTemplateResponseMixin):
    def get_template_names(self):
        obj = self.get_object()
        if obj.template_id:
            template = obj.template.path
            return [template]
        else:
            return super(TemplateAsOptionMixin, self).get_template_names()
