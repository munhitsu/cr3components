from django import forms
from cr3components.cms.models import *
from mptt.forms import MPTTAdminForm


#class PrimaryNodeForm(forms.Form):
#    primary = forms.Select()

class NodeForm(forms.Form):
    class Meta:
        model = Node

#class NodesRelationForm(forms.ModelForm):
#    class Meta:
#        model = NodesRelation

#class NodeChildRelationInlineForm(forms.ModelForm):
#    class Meta:
#        model = NodesRelation

#class NodeParentRelationInlineForm(forms.ModelForm):
#    class Meta:
#        model = NodesRelation

class NodeAdminForm(MPTTAdminForm):
    def __init__(self, *args, **kwargs):
      super(NodeAdminForm, self).__init__(*args, **kwargs)
#      instance = kwargs.get('instance', None)
      parentField = self.fields['parent']
      parentField.queryset = PageNode.on_site.all()

