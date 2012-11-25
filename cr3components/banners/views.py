from cr3components.banners.models import *
from django.http import *

def redirect(request,id):
    """
    redirects to banner.redirect_to or GET['url']
    saves BannerRequest
    """
    try:
        b = Banners.objects.get(pk=int(id))

        if b.redirect_to:
            redirect_to = b.redirect_to
        else:
            redirect_to = request.GET['url']
        
        if b.track:
            b.requests.add(BannerRequest(request=request,user=request.user,redirect_to=redirect_to,banner=b))

        return HttpResponseRedirect(redirect_to)

    except:
        return HttpResponseRedirect(request.GET['url'])
