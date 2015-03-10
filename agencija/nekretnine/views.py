from django.shortcuts import render
from django.template import RequestContext, loader

from nekretnine.models import Drzava, Objekat, Grad, Namestenost, TipObjekta, DeoGrada
from django.http import HttpResponse
import json

filters = {
	'cena': {'name': 'Cena', 'title': 'cena', 'model_filter_key': 'cena', 'type': 'range', 'min_value': 0, 'max_value': 1500, 'start_value': '0-300'},
	'broj_soba': {'name': 'Broj soba', 'title': 'broja soba', 'model_filter_key': 'broj_soba', 'type': 'range', 'min_value': 0, 'max_value': 5, 'start_value': '0-3'},
	'tip_objekta': {'name': 'Tip objekta', 'title': 'tip objekta', 'model_filter_key': 'tip_objekta_id', 'type': 'exact', 'objects': TipObjekta.objects},
	'grad': {'name': 'Gradovi', 'title': 'grad', 'model_filter_key': 'deo_grada__grad_id', 'type': 'exact', 'objects': Grad.objects, 'default': True},
	'deo_grada': {'name': 'Delovi grada', 'title': 'deo grada', 'model_filter_key': 'deo_grada_id', 'type': 'exact', 'objects': DeoGrada.objects, 'depends_on': 'grad', 'depends_on_filter_key': 'grad_id', 'default': True},
	'namestenost': {'name': 'Namestenost', 'title': 'namestenost', 'model_filter_key': 'namestenost_id', 'type': 'exact', 'objects': Namestenost.objects}
}

def index(request):
	drzave = Drzava.objects.all().order_by('-name')
	context = {'drzave': drzave}
	return render(request, 'nekretnine/index.html', context)
	

def objekti(request):
	return render(request, 'nekretnine/objekti.html')

def detalji(request):

	id_stana = request.GET.get('id_stana')
	stan = Objekat.objects.get(id = id_stana);
	context = {'stan' : stan}
	return render(request, 'nekretnine/detalji.html', context)
	
def spisak(request):
	filter_dictionary = {}
	for filter in request.GET:
		value = request.GET.get(filter)
		if filters[filter]['type'] == 'exact':
			filter_dictionary[filters[filter]['model_filter_key']] = value
		else:
			min_value, max_value = value.split('-')
			filter_dictionary[filters[filter]['model_filter_key'] + "__gte"] = min_value
			filter_dictionary[filters[filter]['model_filter_key'] + "__lte"] = max_value
		
	objekti = Objekat.objects.filter(**filter_dictionary)
	context = {'objekti':objekti}
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
		if filters[ime_filtera]['type'] == 'exact':
			template = loader.get_template('nekretnine/filter_lista.html')
			if 'depends_on' in filters[ime_filtera]:
				template_data['depends_on'] = filters[ime_filtera]['depends_on']
			elif 'objects' in filters[ime_filtera]:
				template_data['stavke'] = filters[ime_filtera]['objects'].all()
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
