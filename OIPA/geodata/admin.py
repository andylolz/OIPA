from django.conf.urls import patterns
from django.contrib import admin
from geodata.models import city, country, region
from django.http import HttpResponse
from django.template import RequestContext, loader
from geodata.admin_tools import AdminTools


class CountryAdmin(admin.ModelAdmin):

    def get_urls(self):
        urls = super(CountryAdmin, self).get_urls()

        my_urls = patterns('',
            (r'^update-polygon/$', self.admin_site.admin_view(self.update_polygon)),
            (r'^update-country-center/$', self.admin_site.admin_view(self.update_country_center)),
            (r'^update-regions-set/$', self.admin_site.admin_view(self.update_regions))
        )
        return my_urls + urls

    def update_polygon(self, request):
        admTools = AdminTools()
        admTools.update_polygon_set()
        return HttpResponse('Success')

    def update_country_center(self, request):
        admTools = AdminTools()
        admTools.update_country_center()
        return HttpResponse('Success')

    def update_regions(self, request):
        admTools = AdminTools()
        admTools.update_country_regions()
        return HttpResponse('Success')



class CityAdmin(admin.ModelAdmin):

    def get_urls(self):
        urls = super(CityAdmin, self).get_urls()

        my_urls = patterns('',
            (r'^update-cities/$', self.admin_site.admin_view(self.update_cities))
        )
        return my_urls + urls

    def update_cities(self, request):
        admTools = AdminTools()
        admTools.update_cities()
        return HttpResponse('Success')


admin.site.register(city, CityAdmin)
admin.site.register(country, CountryAdmin)
admin.site.register(region)