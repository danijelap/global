from django.shortcuts import render

from nekretnine.models import Drzava, Objekat



def index(request):
	drzave = Drzava.objects.all().order_by('-naziv')
	context = {'drzave': drzave}
	return render(request, 'nekretnine/index.html', context)
	

def objekti(request):
	context = {}
	return render(request, 'nekretnine/objekti.html', context)

def detalji(request):

	id_stana = request.GET.get('id_stana')
	stan = Objekat.objects.get(id = id_stana);
	context = {'stan' : stan}
	return render(request, 'nekretnine/detalji.html', context)
	
def spisak(request):
	
	objekti = Objekat.objects.all();
	context = {'objekti':objekti}
	return render(request, 'nekretnine/spisak.html', context)
	
	
	
