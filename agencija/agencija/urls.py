from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^nekretnine/', include('nekretnine.urls', namespace="nekretnine")),
    url(r'^admin/', include(admin.site.urls)),
)