from django.conf.urls import patterns, url

from nekretnine import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
)