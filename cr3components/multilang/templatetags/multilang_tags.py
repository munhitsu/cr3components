from django import template
from django.template import Node, NodeList, Template, RequestContext, Variable
from django.conf import settings

from multilang.middleware import is_supported_lang

register = template.Library()

class UrlLangNode(template.Node):
    def __init__(self,item,lang=None):
        self.item = item
        self.lang = lang

    def render(self, context):
        item_val = self.item.resolve(context)
        prefix = ""
        if not self.lang:
            self.lang = context["LANGUAGE_CODE"]
        if is_supported_lang(self.lang):
            if self.lang != settings.LANGUAGE_CODE:
                prefix = "/%s"%self.lang
        if hasattr(item_val,"get_absolute_url"):
            return prefix+item_val.get_absolute_url()
        else:
            return prefix

@register.tag
def url_lang(parser, token):
    """
    returns object.get_absolute_url prefixed with selected language code
    """
    bits = list(token.split_contents())
    if len(bits) == 3:
        item = var = parser.compile_filter(bits[1])
        lang = bits[2]
        return UrlLangNode(item,lang)
    elif len(bits) == 2:
        item = var = parser.compile_filter(bits[1])
        return UrlLangNode(item)
    else:
        raise template.TemplateSyntaxError, "%r tag requires 1 or 2 arguments" % token.contents.split()[0]

