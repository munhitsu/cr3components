from cr3components.banners.models import *
from django.contrib import admin

class BannerImageInlineAdmin(admin.TabularInline):
    model = BannerImage
    extra = 0

class BannerFlashInlineAdmin(admin.TabularInline):
    model = BannerFlash
    exclude=["redirect_to",]
    extra = 0

class BannerRollAdmin(admin.ModelAdmin):
    inlines = [BannerImageInlineAdmin,BannerFlashInlineAdmin,]

admin.site.register(BannerRoll, BannerRollAdmin)
#admin.site.register(Banner)
#admin.site.register(BannerRequest)
#admin.site.register(BannerAlgorithm)
