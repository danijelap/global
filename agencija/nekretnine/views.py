from django.shortcuts import render

from nekretnine.models import Drzava, Objekat, Grad, Namestenost, TipObjekta



def index(request):
	drzave = Drzava.objects.all().order_by('-naziv')
	context = {'drzave': drzave}
	return render(request, 'nekretnine/index.html', context)
	

def objekti(request):
	gradovi = Grad.objects.all()
	namestenosti = Namestenost.objects.all()
	tipovi_objekta = TipObjekta.objects.all()
	context = {'gradovi':gradovi, 'namestenosti': namestenosti, 
		'tipovi_objekta': tipovi_objekta}
	return render(request, 'nekretnine/objekti.html', context)

def detalji(request):

	id_stana = request.GET.get('id_stana')
	stan = Objekat.objects.get(id = id_stana);
	context = {'stan' : stan}
	return render(request, 'nekretnine/detalji.html', context)
	
def spisak(request):
	grad = int(request.GET.get('grad', 0))
	namestenost = int(request.GET.get('namestenost', 0))
	tip_objekta = int(request.GET.get('tip_objekta', 0))
	broj_soba = request.GET.get('broj_soba', 'nista')

	filter_dictionary = {}
	
	if grad != 0:
		filter_dictionary['deo_grada__grad_id'] = grad
		
	if namestenost != 0:
		filter_dictionary['namestenost_id'] = namestenost
		
	if tip_objekta != 0:
		filter_dictionary['tip_objekta_id'] = tip_objekta
		
	if broj_soba != 'nista':
		filter_dictionary['broj_soba'] = broj_soba
		
	objekti = Objekat.objects.filter(**filter_dictionary)
	context = {'objekti':objekti}
	return render(request, 'nekretnine/spisak.html', context)


def filteri(request):
	filteri = ('Gradovi', 'Namestenost', 'Broj soba', 'Tip objekta')
	context = {'filteri': filteri}
	return render(request, 'nekretnine/filteri.html', context)

	z
