from django.shortcuts import render

from nekretnine.models import Drzava, Objekat, DeoGrada, TipObjekta, Namestenost, Grad


def index(request):
	drzave = Drzava.objects.all().order_by('-naziv')
	context = {'drzave': drzave}
	return render(request, 'nekretnine/index.html', context)
	
def objekti(request):
	tip_objekta = int(request.GET.get('tip_objekta', 0))
	namestenost = int(request.GET.get('namestenost', 0))
	grad = int(request.GET.get('grad', 0)) 
	cena = request.GET.get('cena', 'nista')
	broj_soba = request.GET.get('broj_soba', 'nista')
	
	filter_dictionary = {}
	
	if tip_objekta != 0:
		filter_dictionary['tip_objekta_id'] = tip_objekta
		
	if namestenost != 0:
		filter_dictionary['namestenost_id'] = namestenost
		
	if grad != 0:
		filter_dictionary['deo_grada__grad_id'] = grad 
	
	if cena != 'nista':
		(cena_min, cena_max) = cena.split('-')
		cena_min = int(cena_min)
		cena_max = int(cena_max) 
		filter_dictionary['cena__gte'] = cena_min	
		filter_dictionary['cena__lte'] = cena_max
		
	if broj_soba != 'nista':
		filter_dictionary['broj_soba'] = broj_soba
	
		
	objekti = Objekat.objects.filter(**filter_dictionary)
	
	tipovi_objekta = TipObjekta.objects.all();
	namestenosti = Namestenost.objects.all();
	gradovi = Grad.objects.all();
	
	context = {'objekti': objekti, 'tipovi_objekta': tipovi_objekta, 
		'izabran_tip_objekta': tip_objekta, 'izabrana_namestenost': namestenost,
		'namestenosti': namestenosti, 'izabran_grad': grad, 'gradovi': gradovi, 
		'izabrana_cena': cena, 'broj_soba': broj_soba}
	return render(request, 'nekretnine/objekti.html', context)
	