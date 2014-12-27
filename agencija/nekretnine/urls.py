from django.conf.urls import patterns, url

from nekretnine import views

urlpatterns = patterns('',
	url(r'^detalji/$', views.detalji, name='detalji'),	
	url(r'^objekti/$', views.objekti, name='objekti'),
	url(r'^spisak/$', views.spisak, name='spisak'),
	url(r'^filteri/$', views.filteri, name='filteri'),
	url(r'^napravi_filter/$', views.napravi_filter, name='napravi_filter'),
)