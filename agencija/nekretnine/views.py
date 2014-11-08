from django.shortcuts import render

from nekretnine.models import Drzava, Objekat, DeoGrada


def index(request):
	drzave = Drzava.objects.all().order_by('-naziv')
	context = {'drzave': drzave}
	return render(request, 'nekretnine/index.html', context)
	
def objekti(request):
	deo_grada = request.GET.get('deo_grada', None)
	if deo_grada is not None:
		objekti = Objekat.objects.filter(deo_grada_id = deo_grada)
	else:
		objekti = Objekat.objects.all()
	delovi_grada = DeoGrada.objects.all();
	context = {'objekti': objekti, 'delovi_grada': delovi_grada}
	return render(request, 'nekretnine/objekti.html', context)
	