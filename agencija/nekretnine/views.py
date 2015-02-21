from django.shortcuts import render
from django.template import RequestContext, loader

from nekretnine.models import Drzava, Objekat, Grad, Namestenost, TipObjekta
from django.http import HttpResponse
import json

filters = {
	'cena': {'name': 'Cena', 'title': 'cena', 'model_filter_key': 'cena', 'type': 'range', 'min_value': 0, 'max_value': 1500, 'start_value': '0-300'},
	'broj_soba': {'name': 'Broj soba', 'title': 'broja soba', 'model_filter_key': 'broj_soba', 'type': 'range', 'min_value': 0, 'max_value': 5, 'start_value': '0-3'},
	'tip_objekta': {'name': 'Tip objekta', 'title': 'tip objekta', 'model_filter_key': 'tip_objekta_id', 'type': 'exact', 'objects': TipObjekta.objects},
	'grad': {'name': 'Gradovi', 'title': 'grad', 'model_filter_key': 'deo_grada__grad_id', 'type': 'exact', 'objects': Grad.objects},
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


def filteri(request):
	filters_to_show_get = request.GET.getlist('filteri[]')
	filters_to_show_data = []
	for filter_key in filters:
		if filter_key in filters_to_show_get:
			filters_to_show_data.append({'id': filter_key, 'name': filters[filter_key]['name']})
	context = {'filteri': filters_to_show_data}
	return render(request, 'nekretnine/filteri.html', context)

def napravi_filtere(request):
	niz_filtera = request.GET.getlist('niz_filtera[]')
	response_content = '';
	for ime_filtera in niz_filtera:
		template_data = {'id': ime_filtera, 'title': filters[ime_filtera]['title']}
		if 'objects' in filters[ime_filtera]:
			template_data['stavke'] = filters[ime_filtera]['objects'].all()
		if filters[ime_filtera]['type'] == 'exact':
			template = loader.get_template('nekretnine/filter_lista.html')
		else:
			template = loader.get_template('nekretnine/filter_range.html')
			template_data['min_value'] = filters[ime_filtera]['min_value']
			template_data['max_value'] = filters[ime_filtera]['max_value']
			template_data['start_value'] = filters[ime_filtera]['start_value']
		
		context = RequestContext(request, template_data)
		response_content += template.render(context)
	return HttpResponse(response_content)
		