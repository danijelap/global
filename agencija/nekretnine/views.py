from django.shortcuts import render

from nekretnine.models import Drzava, Objekat, Grad, Namestenost, TipObjekta
from django.http import HttpResponse

filters = {
	'cena': {'name': 'Cena', 'title': 'cena', 'model_filter_key': 'cena', 'type': 'range'},
	'tip_objekta': {'name': 'Tip objekta', 'title': 'tip objekta', 'model_filter_key': 'tip_objekta_id', 'type': 'exact', 'objects': TipObjekta.objects},
	'grad': {'name': 'Gradovi', 'title': 'grad', 'model_filter_key': 'deo_grada__grad_id', 'type': 'exact', 'objects': Grad.objects},
	'namestenost': {'name': 'Namestenost', 'title': 'namestenost', 'model_filter_key': 'namestenost_id', 'type': 'exact', 'objects': Namestenost.objects}
}

def index(request):
	drzave = Drzava.objects.all().order_by('-naziv')
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

def napravi_filter(request):
	ime_filtera = request.GET.get('ime_filtera')
	context = {'id': ime_filtera, 'name': filters[ime_filtera]['name']}
	if 'objects' in filters[ime_filtera]:
		context['stavke'] = filters[ime_filtera]['objects'].all()
	if filters[ime_filtera]['type'] == 'exact':
		template = 'nekretnine/filter_lista.html'
	else:
		template = 'nekretnine/filter_range.html'
	
	return render(request, template, context)
