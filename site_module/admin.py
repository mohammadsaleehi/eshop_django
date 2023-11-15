from django.contrib import admin

from site_module.models import *


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
	pass


@admin.register(FooterLink)
class FooterLinkAdmin(admin.ModelAdmin):
	list_display = ['title', 'footer_link_box']


admin.site.register(FooterLinkBox)
admin.site.register(SiteBanner)

admin.site.register(Slider)
