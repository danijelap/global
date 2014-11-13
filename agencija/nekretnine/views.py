from django.shortcuts import render

from nekretnine.models import Drzava, Objekat, DeoGrada, TipObjekta, Namestenost


def index(request):
	drzave = Drzava.objects.all().order_by('-naziv')
	context = {'drzave': drzave}
	return render(request, 'nekretnine/index.html', context)
	
def objekti(request):
	deo_grada = int(request.GET.get('deo_grada', 0))
	tip_objekta = int(request.GET.get('tip_objekta', 0))
	namestenost = int(request.GET.get('namestenost', 0))
	filter_dictionary = {}
	
	if deo_grada != 0:
		filter_dictionary['deo_grada_id'] = deo_grada
	
	if tip_objekta != 0:
		filter_dictionary['tip_objekta_id'] = tip_objekta
		
	if namestenost != 0:
		filter_dictionary['namestenost_id'] = namestenost
		
	objekti = Objekat.objects.filter(**filter_dictionary)
	
	tipovi_objekta = TipObjekta.objects.all();
	delovi_grada = DeoGrada.objects.all();
	namestenosti = Namestenost.objects.all();
	
	context = {'objekti': objekti, 'delovi_grada': delovi_grada, 
		'tipovi_objekta': tipovi_objekta, 'izabran_deo_grada': deo_grada, 
		'izabran_tip_objekta': tip_objekta, 'izabrana_namestenost':namestenost}
	return render(request, 'nekretnine/objekti.html', context)
	