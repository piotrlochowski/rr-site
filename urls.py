from django.conf.urls.defaults import patterns, include, url
from tastypie.api import Api
from racerecordweb.api import LapResource, TrialResource, TrialResultResource, LocationResource, DriverResource

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


lap_resource = LapResource()

v1_api = Api(api_name='v1')
v1_api.register(TrialResultResource())
v1_api.register(LapResource())
v1_api.register(TrialResource())
v1_api.register(LocationResource())
v1_api.register(DriverResource())

urlpatterns = patterns('',
    url(r'^py/racerecordweb/', include('racerecordweb.urls')),
    url(r'^py/api/', include(v1_api.urls)),
    # Examples:
    # url(r'^$', 'racerecordsite.views.home', name='home'),
    # url(r'^racerecordsite/', include('racerecordsite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^py/admin/', include(admin.site.urls)),
)