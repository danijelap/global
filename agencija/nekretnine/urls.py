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
	url(r'^report_inactive/$', views.report_inactive, name='report_inactive'),
	url(r'^report_middleman/$', views.report_middleman, name='report_middleman'),
	url(r'^send_message/$', views.send_message, name='send_message'),
	url(r'^register/$', views.register, name='register'),
	url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'nekretnine/login.html'}),
	url(r'^ad/$', views.ad, name='ad'),
	url(r'^ads/$', views.ads, name='ads'),
	url(r'^personal_info/$', views.personal_info, name='personal_info'),
	url(r'^change_pass/$', views.change_password, name='change_pass'),
	url(r'^logout/$', views.logout_view, name='logout'),
	url(r'^$', views.construction, name='construction'),
)