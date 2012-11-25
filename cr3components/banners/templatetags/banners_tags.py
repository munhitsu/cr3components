from cr3components.banners.models import *
from django import template
from django.template import Node, NodeList, Template, RequestContext, Variable

register = template.Library()

class BannerRollNode(template.Node):
    default_template = "banners/inc_banner_roll.html"
    def __init__(self,slug,template=None,variable=None):
        self.slug = slug
        self.template = template
        self.variable = variable

    def render(self, context):
        slug = self.slug.resolve(context)
        if self.template:
            template = self.template.resolve(context)
        else:
            template = self.default_template
        br,created = BannerRoll.objects.get_or_create(slug=slug)
        return br.render(context,template)


@register.tag
def bannerroll(parser, token):
    """
    {% bannerroll "slug_val" "template_name"? %}
    {% bannerroll slug_var template_name_var? %}
    {% bannerroll slug_var as var_name %}{% for banner in var_name.banners %}{% endfor %}
    last form is used when one wants to override banner template
    beware that in such case publishability of object is to be verified in template
    """
    bits = list(token.split_contents())
    if len(bits) == 3:
        slug = parser.compile_filter(bits[1])
        template = parser.compile_filter(bits[2])
        return BannerRollNode(slug, template)
    elif len(bits) == 2:
        slug = parser.compile_filter(bits[1])
        return BannerRollNode(slug)
    elif len(bits) == 4 and bits[2] == "as":
        slug = parser.compile_filter(bits[1])
        var_name = bits[3]
        return ObjectBySlugNode(slug, var_name, BannerRoll)
    else:
        raise template.TemplateSyntaxError, "%r tag requires 1 or 2 arguments" % token.contents.split()[0]
    
