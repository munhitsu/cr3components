# Create your views here.
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django.utils.translation import ugettext as _
from django.http import HttpResponseRedirect, HttpResponse, Http404

from cr3components.cms.models import Node
import logging

log = logging.getLogger(__name__)

def node_view(request, path, path_prefix, slug):
    if path_prefix is None:
        path_prefix = ''
    nodes = Node.objects.filter(slug=slug, path_prefix_store=path_prefix).select_subclasses()
    try:
        node = nodes[0]
        if node.redirect_to:
            return HttpResponseRedirect(node.redirect_to)
        else:
            return render_to_response(node.get_template(), {'node':node},
                                      context_instance=RequestContext(request))
    except IndexError:
        log.error("node_view(request,%s,%s,%s)" % (path, path_prefix, slug))
        raise Http404


def node_print_view(request, path, path_prefix, slug):
    if path_prefix is None:
        path_prefix = ''
    nodes = Node.objects.filter(slug=slug, path_prefix_store=path_prefix).select_subclasses()
    try:
        node = nodes[0]
        if node.redirect_to:
            return HttpResponseRedirect(node.redirect_to)
        else:
            return render_to_response("cms/print_node.html", {'node':node},
                                      context_instance=RequestContext(request))    
    except IndexError:
        log.error("node_view(request,%s,%s,%s)" % (path, path_prefix, slug))
        raise Http404

