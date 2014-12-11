from django.shortcuts import render

from nekretnine.models import Drzava, Objekat



def index(request):
	drzave = Drzava.objects.all().order_by('-naziv')
	context = {'drzave': drzave}
	return render(request, 'nekretnine/index.html', context)
	

def objekti(request):
	objekti = Objekat.objects.all()
	context = {'objekti' : objekti}
	return render(request, 'nekretnine/objekti.html', context)

def detalji(request):
	stan_id = request.GET.get('stan_id', None)
	if stan_id is not None:
		stan = Objekat.objects.get(id = stan_id)
		context = {'stan' : stan}
		return render(request, 'nekretnine/detalji.html', context)
	
