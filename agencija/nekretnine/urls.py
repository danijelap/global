from django.conf.urls import patterns, url

from nekretnine import views

urlpatterns = patterns('',

    url(r'^objekti/$', views.objekti, name='objekti'),
)