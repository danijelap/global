from django.shortcuts import render

from nekretnine.models import Drzava


def index(request):
	spisak = Drzava.objects.all()
	context = {'spisak': spisak}
	return render(request, 'nekretnine/index.html', context)