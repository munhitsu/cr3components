from django import forms 
from django.utils.safestring import mark_safe 
from django.conf import settings

class WMDTextEditorWidget(forms.Textarea): 
        class Media: 
                css = {
                    "all": ("wmd.css",)
                }
                js = ('%sjs/wmd/wmd.js' % settings.STATIC_URL,
                      '%sjs/wmd/showdown.js' % settings.STATIC_URL,
                      )
                
        def render(self, name, value, attrs=None): 
                output = [super(WMDTextEditorWidget, self).render(name, value, attrs)] 
                output.append(u'<div id="previewPane" class="pane wmd-preview"></div>') 
                return mark_safe(u''.join(output)) 
