from django.shortcuts import render
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.db.models import Q
from django.forms.models import model_to_dict

from nekretnine.forms import *
from nekretnine.models import *

import json
from datetime import date

filters = {
	'cena': {'name': 'Cena', 'title': 'cena', 'model_filter_key': 'cena (€)', 'type': 'range', 'min_value': 0, 'max_value': 1500, 'start_value': '0-300'},
	'broj_soba': {'name': 'Broj soba', 'title': 'broj soba', 'model_filter_key': 'broj_soba', 'type': 'range', 'min_value': 0, 'max_value': 5, 'start_value': '0-3'},
	'tip_objekta': {'name': 'Tip objekta', 'title': 'tip objekta', 'model_filter_key': 'tip_objekta_id', 'type': 'exact', 'objects': TipObjekta.objects},
	'grad': {'name': 'Gradovi', 'title': 'grad', 'model_filter_key': 'deo_grada__grad_id', 'type': 'exact', 'objects': Grad.objects, 'default': True},
	'deo_grada': {'name': 'Delovi grada', 'title': 'deo grada', 'model_filter_key': 'deo_grada_id', 'type': 'exact', 'objects': DeoGrada.objects, 'depends_on': 'grad', 'depends_on_filter_key': 'grad_id', 'default': True},
	'namestenost': {'name': 'Nameštenost', 'title': 'nameštenost', 'model_filter_key': 'namestenost_id', 'type': 'exact', 'objects': Namestenost.objects},
	'povrsina': {'name': 'Površina', 'title': 'površina', 'model_filter_key': 'povrsina', 'type': 'range', 'min_value': 0, 'max_value': 400, 'start_value': '50-100'},
	'heating': {'name': 'Grejanje', 'title': 'grejanje', 'model_filter_key': 'heating_id', 'type': 'exact', 'objects': Heating.objects},
	'floor': {'name': 'Sprat', 'title': 'sprat', 'model_filter_key': 'floor', 'type': 'range', 'min_value': 0, 'max_value': 30, 'start_value': '1-4'},
	'construction_year': {'name': 'Godina izgradnje', 'title': 'godina izgradnje', 'model_filter_key': 'construction_year', 'type': 'range', 'min_value': 1900, 'max_value': date.today().year, 'start_value': '1970-{0}'.format(date.today().year)},
	'additional_features': {'name': 'Ostale pogodnosti', 'title': 'ostale pogodnosti', 'model_filter_key': 'additional_features', 'type': 'multi', 'objects': AdditionalFeatures.objects},
}

menu_items = [
	{'text': 'početna strana', 'id': 'home_page', 'href': '/objekti/'}, 
	{'text': 'lični podaci', 'id': 'personal_info', 'href': '/personal_info/'},
	{'text': 'promena lozinke', 'id': 'change_pass', 'href': '/change_pass/'},
	{'text': 'moji oglasi', 'id': 'ads', 'href': '/ads/'}, 
	{'text': 'unos oglasa', 'id': 'ad', 'href': '/ad/'}
]

def register(request):
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			new_user, new_owner = form.save()
			return HttpResponseRedirect("/login/")
	else:
		form = UserRegistrationForm()
	return render(request, "nekretnine/register.html", {
		'form': form,
	})

def login(request): ############# NOT USED!!!
	if not request.user.is_authenticated():
		if request.method == 'POST':
			form = UserLoginForm(request.POST)
			if form.is_valid():
				user = form.login(request)
				if user is not None:
					return HttpResponseRedirect("/ad/")
		else:
			form = UserLoginForm()
		return render(request, "nekretnine/login.html")
	else:
		return HttpResponseRedirect("/ad/")

@login_required
def ad(request):
	context = {}
	if request.method == 'POST':
		user = request.user
		if user.is_authenticated():
			object_id = request.POST.get('object_id')
			if object_id != "":  # saving edited ad
				object = Objekat.objects.get(pk=object_id)
				object_form = ObjectForm(request.POST, instance=object)
				new_images_form = NewImagesForm(request.POST, request.FILES)
				ad_form = AdForm(request.POST, instance=object.ad_set.first())
				if object_form.is_valid() and ad_form.is_valid() and new_images_form.is_valid():
					object_form.save()
					ad_form.save()
					for image in new_images_form.get_images():
						image.object = object
						image.save()
					for object_image_id in request.POST.getlist("delete_images[]"):
						ObjectImage.objects.get(pk=object_image_id).delete()
					return HttpResponseRedirect("/ad/?id=" + object_id)
				else:
					context['object_form'] = object_form
					context['new_images_form'] = new_images_form
					context['ad_form'] = ad_form
					context['object_id'] = object_id
			else:  # saving new ad
				object_form = ObjectForm(request.POST)
				new_images_form = NewImagesForm(request.POST, request.FILES)
				if object_form.is_valid() and new_images_form.is_valid():
					owner = Owner.objects.get(user=request.user)
					object = object_form.save(commit=False)
					object.owner = owner
					object.save()
					for image in new_images_form.get_images():
						image.object = object
						image.save()
					ad = Ad(object=object)
					ad.save()
				return HttpResponseRedirect("/ads/")
		else:
			raise forms.ValidationError(
				"Vaš nalog nije aktiviran. Proverite email i ispratite uputstva.",
				code='account_disabled',
			)
	else:
		object_id = request.GET.get('id')
		if object_id is not None:  # edit an existing ad
			object = Objekat.objects.get(pk=object_id)
			context['object_form'] = ObjectForm(instance=object)
			context['images'] = []
			for object_image in object.objectimage_set.all():
				context['images'].append({'url': object_image.image.url, 'id': object_image.id})
			context['new_images_form'] = NewImagesForm()
			context['ad_form'] = AdForm(instance=object.ad_set.first())
			context['object_id'] = object_id
		else:  # create new ad
			context['object_form'] = ObjectForm()
			context['new_images_form'] = NewImagesForm()

	context['selected_item'] = 'ad'
	context['menu_items'] = menu_items
	return render(request, "nekretnine/ad.html", context)

@login_required
def ads(request):
	ads = Ad.objects.filter(object__owner__user=request.user)
	return render(request, "nekretnine/ads.html", {'menu_items': menu_items, 'selected_item': 'ads', 'ads': ads})

@login_required
def personal_info(request):
	owner = Owner.objects.get(user=request.user)
	if request.method == 'POST':
		owner_form = OwnerForm(request.POST, instance=owner)
		user_form = UserForm(request.POST, instance=owner.user)
		if owner_form.is_valid() and user_form.is_valid():
			owner_form.save()
			user_form.save()
		return HttpResponseRedirect("/personal_info/")
	else:
		owner_form = OwnerForm(instance=owner)
		user_form = UserForm(instance=owner.user)
		context = {'owner_form': owner_form, 'user_form': user_form}
		context['selected_item'] = 'personal_info'
		context['menu_items'] = menu_items
		return render(request, 'nekretnine/personal_info.html', context)

@login_required
def change_password(request):
	if request.method == 'POST':
		change_pass_form = ChangePasswordForm(request.POST, user=request.user)
		if change_pass_form.is_valid():
			change_pass_form.save()
			return HttpResponseRedirect("/objekti/")
	else:
		change_pass_form = ChangePasswordForm(user=request.user)
	context = {'change_pass_form': change_pass_form}
	context['selected_item'] = 'change_pass'
	context['menu_items'] = menu_items
	return render(request, 'nekretnine/change_pass.html', context)


def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/objekti/')

def get_client_ip(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[-1].strip()
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip

def construction(request):
	return render(request, 'nekretnine/construction.html')

def index(request):
	drzave = Drzava.objects.all().order_by('-name')
	context = {'drzave': drzave}
	return render(request, 'nekretnine/index.html', context)
	

def objekti(request):
	return render(request, 'nekretnine/objekti.html')

def detalji(request):

	id_stana = request.GET.get('id_stana')
	stan = Objekat.objects.get(id = id_stana)
	ad = Ad.objects.get(object = stan)
	context = {'stan' : stan, 'ad': ad}
	return render(request, 'nekretnine/detalji.html', context)
	
def spisak(request):
	query = Q(ad__active=True)
	many_to_many_filters = {}
	for filter_name in request.GET:
		if filter_name[-2:] == '[]':
			filter_name = filter_name[:-2]
		if filters[filter_name]['type'] == 'exact':
			value = request.GET.get(filter_name)
			query_filter = {filters[filter_name]['model_filter_key']: value}
			query = query & Q(**query_filter)
		elif filters[filter_name]['type'] == 'range':
			value = request.GET.get(filter_name)
			min_value, max_value = value.split('-')
			query_filter = {
				filters[filter_name]['model_filter_key'] + "__gte": min_value,
				filters[filter_name]['model_filter_key'] + "__lte": max_value
			}
			query = query & Q(**query_filter)
		elif filters[filter_name]['type'] == 'multi':
			values = request.GET.getlist(filter_name + '[]')
			many_to_many_filters[filters[filter_name]['model_filter_key']] = set([int(value) for value in values])

	objects_to_exclude = []
	objects = Objekat.objects.filter(query)

	for model_filter_key, values_to_filter in many_to_many_filters.items():
		for one_object in objects:
			object_values = set(model_to_dict(one_object, model_filter_key)[model_filter_key])
			if not values_to_filter.issubset(object_values):
				objects_to_exclude.append(one_object.id)

	if len(objects_to_exclude) > 0:
		context = {'objekti': objects.exclude(id__in=objects_to_exclude)}
	else:
		context = {'objekti': objects}

	return render(request, 'nekretnine/spisak.html', context)


def get_filter_choice(request):
	filters_to_show_get = request.GET.getlist('filters[]')
	filters_to_show_data = []
	for filter_key in filters:
		if filter_key in filters_to_show_get:
			start_value = filters[filter_key].get('start_value', 0)
			filters_to_show_data.append({'id': filter_key, 'name': filters[filter_key]['name'], 'start_value': start_value})
	context = {'filteri': filters_to_show_data}
	return render(request, 'nekretnine/get_filter_choice.html', context)

def make_filters(request):
	niz_filtera = request.GET.getlist('filter_array[]')
	response_content = '';
	for ime_filtera in niz_filtera:
		template_data = {'id': ime_filtera, 'title': filters[ime_filtera]['title']}
		if filters[ime_filtera]['type'] in ('exact', 'multi'):
			template = loader.get_template('nekretnine/filter_lista.html')
			if 'depends_on' in filters[ime_filtera]:
				template_data['depends_on'] = filters[ime_filtera]['depends_on']
			elif 'objects' in filters[ime_filtera]:
				template_data['stavke'] = filters[ime_filtera]['objects'].all()
			template_data['type'] = filters[ime_filtera]['type']
		else:
			template = loader.get_template('nekretnine/filter_range.html')
			template_data['min_value'] = filters[ime_filtera]['min_value']
			template_data['max_value'] = filters[ime_filtera]['max_value']
			template_data['start_value'] = filters[ime_filtera]['start_value']
		
		context = RequestContext(request, template_data)
		response_content += template.render(context)
	return HttpResponse(response_content)

def get_filter_content(request):
	dependent_filter_id = request.GET.get('dependent_filter_id')
	depends_on_filter_value = request.GET.get('depends_on_filter_value')
	filter_dictionary = {filters[dependent_filter_id]['depends_on_filter_key']: depends_on_filter_value}
	items = filters[dependent_filter_id]['objects'].filter(**filter_dictionary)
	context = {'items': items, 'title': filters[dependent_filter_id]['title']}
	return render(request, 'nekretnine/filter_list_content.html', context)

def get_filter_list(request):
	result = {}
	for filter_id in filters:
		filter_object = {}
		if 'default' in filters[filter_id]:
			filter_object['default'] = True
		if 'depends_on' in filters[filter_id]:
			filter_object['depends_on'] = filters[filter_id]['depends_on']
		if 'start_value' in filters[filter_id]:
			filter_object['start_value'] = filters[filter_id]['start_value']
		result[filter_id] = filter_object
	return HttpResponse(json.dumps(result))

def report_inactive(request):
	ad = Ad.objects.get(object__id = request.POST.get('object_id'))
	my_token = request.POST.get('my_token')
	ad_reporters = AdReporter.objects.filter(ad = ad, reporter_token = my_token)
	if len(ad_reporters) == 0:
		ad_reporter = AdReporter(ad = ad, reporter_token = my_token, reporter_ip_address = get_client_ip(request))
		ad_reporter.save()
		ad.reported_as_inactive_counter += 1
		ad.save()
	return HttpResponse("OK")

def report_middleman(request):
	ad = Ad.objects.get(object__id = request.POST.get('object_id'))
	my_token = request.POST.get('my_token')
	ad_reporters = AdReporter.objects.filter(ad = ad, reporter_token = my_token)
	if len(ad_reporters) == 0:
		ad_reporter = AdReporter(ad = ad, reporter_token = my_token, reporter_ip_address = get_client_ip(request))
		ad_reporter.save()
		ad.reported_as_middleman_counter += 1
		ad.save()
	return HttpResponse("OK")
