from django.conf import settings

def basic(request):
    if request.GET.has_key("query"):
        import search
        search.manager.query = request.GET["query"]
        return {
            'search' : search.manager,
        }
    else:
        return {
        }
