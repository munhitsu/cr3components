from django import template
from django.template import Node, NodeList, Template, RequestContext, Variable
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

from cr3components.cms.models import Node, PageNode

register = template.Library()

class CmsNode(template.Node):
    def __init__(self, path, nodelist, variable="cms_node"):
        self.path = path
        self.variable = variable
        self.nodelist = nodelist

    def render(self, context):
        path = self.path.resolve(context)
        node = PageNode.objects.get_or_create_path(path)
        context.push()
        context[self.variable] = node
        output = self.nodelist.render(context)
        context.pop()
        return output

@register.tag
def cms(parser, token):
    """
    cms "dupa/dupa"
    cms "dupa/dupa" as dupa
    cms dupa_var as dupa
    """
    nodelist = parser.parse(('endcms',))
    parser.delete_first_token()
    bits = list(token.split_contents())
    if len(bits) == 4 and bits[2] == "as":
        path = parser.compile_filter(bits[1])
        variable = bits[3]
        return CmsNode(path, nodelist, variable)
    elif len(bits) == 2:
        path = parser.compile_filter(bits[1])
        return CmsNode(path, nodelist)
    else:
        raise template.TemplateSyntaxError, "%r tag requires 1 or 3 arguments" % token.contents.split()[0]


class GoogleAnalyticsNode(template.Node):
    def render(self, context):
        return render_to_string("cms/googleanalytics.html", {"CMS_GOOGLE_ANALYTICS_ID":Site.objects.get_current().cmssite.google_analytics_id}, context)

@register.tag
def googleanalytics(parser, token):
    return GoogleAnalyticsNode()
