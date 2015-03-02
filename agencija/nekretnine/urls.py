from django.conf.urls import patterns, url

from nekretnine import views

urlpatterns = patterns('',
	url(r'^detalji/$', views.detalji, name='detalji'),	
	url(r'^objekti/$', views.objekti, name='objekti'),
	url(r'^spisak/$', views.spisak, name='spisak'),
	url(r'^get_filter_choice/$', views.get_filter_choice, name='get_filter_choice'),
	url(r'^make_filters/$', views.make_filters, name='make_filters'),
	url(r'^get_filter_content/$', views.get_filter_content, name='get_filter_content'),
	url(r'^get_filter_list/$', views.get_filter_list, name='get_filter_list'),
)