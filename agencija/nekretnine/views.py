from django.shortcuts import render

from nekretnine.models import Drzava, Objekat, Grad, Namestenost, TipObjekta



def index(request):
	drzave = Drzava.objects.all().order_by('-naziv')
	context = {'drzave': drzave}
	return render(request, 'nekretnine/index.html', context)
	

def objekti(request):
	grad = int(request.GET.get('grad', 0))
	namestenost = int(request.GET.get('namestenost', 0))
	broj_soba = request.GET.get('broj_soba', 'nista')
	tip_objekta = int(request.GET.get('tip_objekta', 0))
	
	filter_dictionary = {}
	
	if grad != 0:
		filter_dictionary['grad_id'] = grad
		
	if namestenost != 0:
		filter_dictionary['namestenost_id'] = namestenost
		
	if broj_soba != 'nista':
		filter_dictionary['broj_soba'] = broj_soba
	
	if tip_objekta != 0:
		filter_dictionary['tip_objekta_id'] = tip_objekta
		
	objekti = Objekat.objects.filter(**filter_dictionary)
	
	gradovi = Grad.objects.all()
	namestenosti = Namestenost.objects.all()
	tipovi_objekta = TipObjekta.objects.all()
	
	context = {'objekti' : objekti, 'grad':grad, 'gradovi':gradovi,
		'izabrana_namestenost': namestenost,'namestenosti': namestenosti, 
		'izabran_broj_soba': broj_soba, 'tipovi_objekta': tipovi_objekta, 
		'izabran_tip_objekta': tip_objekta}
	return render(request, 'nekretnine/objekti.html', context)

def detalji(request):

	id_stana = request.GET.get('id_stana')
	stan = Objekat.objects.get(id = id_stana);
	context = {'stan' : stan}
	return render(request, 'nekretnine/detalji.html', context)
