from django import template
from django.template import Node, NodeList, Template, RequestContext, Variable
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.template.base import TemplateSyntaxError

from cr3components.cms.models import Node
from bt3.products.models import Category
from django.contrib.gis.shortcuts import render_to_text

register = template.Library()

from cr3components.foundation.templatetags.functions import parse_kwargs


class ObjectBySlugNode(template.Node):
    def __init__(self, slug, var_name, klass):
        self.slug = slug
        self.var_name = var_name
        self.klass = klass
    
    def render(self, context):
        var = self.slug.resolve(context, True)
        try:
            object = self.klass.objects.get(slug=var) #try it in java :)            
        except:
            object = None
        context[self.var_name] = object
        return ""

def object_by_slug(parser, token, default_var_name, klass):
    """
    generic code for all get object by slug
    """
    firstbits = token.contents.split(None, 4)
    tag_name = firstbits[0]
    if len(firstbits) == 1:
        raise TemplateSyntaxError("'%s' tag takes at least 1 argument" % tag_name)
    if len(firstbits) == 2:
        slug = parser.compile_filter(firstbits[1])
        var_name = default_var_name
    elif len(firstbits) == 3:
        raise TemplateSyntaxError("'%s' tag takes 1 or 3 arguments" % tag_name)
    elif len(firstbits) == 4:
        if firstbits[2] != 'as':
            raise TemplateSyntaxError("second argument to '%s' tag must be 'as'" % tag_name)
        else:
            slug = parser.compile_filter(firstbits[1])
            var_name = firstbits[3]
   
    return ObjectBySlugNode(slug, var_name, klass)
