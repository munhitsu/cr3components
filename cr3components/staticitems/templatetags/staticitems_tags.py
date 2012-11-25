from django import template
from django.core.cache import cache
from django.template import Node, NodeList, Template, RequestContext, Variable
from cr3components.staticitems.models import StaticItem, Image, File, Flash, Snippet
import hashlib
register = template.Library()

class StaticItemNode(template.Node):
    
    def __init__(self,slug,templatename=None,variable=None,nodelist=None,model=None):
        self.slug = slug
        self.templatename = templatename
        self.variable = variable
        self.nodelist2 = nodelist
        self.model = model

    def render(self, context):
        slug = self.slug.resolve(context)
        m = hashlib.md5()
        m.update(slug)
        if self.templatename:
            m.update(self.templatename)
        if self.variable:
            m.update(self.variable)
        if self.nodelist2:
            m.update(self.nodelist2)
        if self.model:
            m.update(self.model.__name__)
        c_key = "staticitem_%s_%s" % (slug,m.hexdigest())
        c_out = cache.get(c_key,None)
        if c_out:
            return c_out
        else:
            c_out = self._render(context,slug)
            cache.set(c_key,c_out)
            return c_out
    
    def _render(self, context, slug):
        si = None
        try:
            si = StaticItem.objects.get(slug=slug)
            si = si.as_leaf_class()
        except StaticItem.DoesNotExist:
            if self.model:
                si = self.model(slug=slug)
                si.save()
        if si:
            if self.variable and self.nodelist2:               
                context.push()
                context[self.variable] = si
                output = self.nodelist2.render(context)
                context.pop()
                return output
            else:
                return si.render(context,self.templatename)
        else:
            return ""

STATICITEM_MODELS = {
    "staticitem_snippet":Snippet,
    "staticitem_file":File,
    "staticitem_image":Image,
    "staticitem_flash":Flash,
    "staticitem":None
}

@register.tag
def staticitem(parser, token):
    """
    {% staticitem_snippet ... %}
    {% staticitem_file ... %}
    {% staticitem_image ... %}
    {% staticitem_flash ... %}
    {% staticitem "slug_val" template? %}
    {% staticitem slug_var template? %}
    {% staticitem slug as variable %}
    """
    bits = list(token.split_contents())
    model = STATICITEM_MODELS[bits[0]]
    
    if len(bits) == 3:
        slug = parser.compile_filter(bits[1])
        templatename = parser.compile_filter(bits[2])
        return StaticItemNode(slug, templatename, model=model)
    elif len(bits) == 2:
        slug = parser.compile_filter(bits[1])
        return StaticItemNode(slug, model=model)
    elif len(bits) == 4 and bits[2] == "as":
        slug = parser.compile_filter(bits[1])
        variable = bits[3]
        nodelist = parser.parse(('endstaticitem',))
        parser.delete_first_token()
        return StaticItemNode(slug, variable=variable, nodelist=nodelist, model=model)
    else:
        raise template.TemplateSyntaxError, "%r tag requires 1,2 arguments or 4 when third is 'as'" % token.contents.split()[0]

@register.tag
def staticitem_snippet(parser, token):
    return staticitem(parser, token)

@register.tag
def staticitem_file(parser, token):
    return staticitem(parser, token)

@register.tag
def staticitem_image(parser, token):
    return staticitem(parser, token)

@register.tag
def staticitem_flash(parser, token):
    return staticitem(parser, token)
