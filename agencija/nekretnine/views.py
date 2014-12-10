from django.shortcuts import render

from nekretnine.models import Drzava, Objekat,



def index(request):
	drzave = Drzava.objects.all().order_by('-naziv')
	context = {'drzave': drzave}
	return render(request, 'nekretnine/index.html', context)
	

def objekti(request):
	objekti = Objekat.objects.all()
	context = {'objekti' : objekti}
	return render(request, 'nekretnine/objekti.html', context)


