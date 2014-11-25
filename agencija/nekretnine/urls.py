from django.conf.urls import patterns, url

from nekretnine import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^objekti/$', views.objekti, name='objekti'),
	url(r'^detalji/$', views.detalji, name='detalji'),
)