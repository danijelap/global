from django.contrib import admin
from nekretnine.models import Drzava, Grad, Objekat,DeoGrada,Namestenost,TipObjekta

class GradInline(admin.TabularInline):
	model = Grad

class DrzavaAdmin(admin.ModelAdmin):
	inlines = [GradInline]
	
class DeoGradaInline(admin.TabularInline):	
	model = DeoGrada

class GradAdmin(admin.ModelAdmin):
	inlines = [DeoGradaInline]
	
admin.site.register(Drzava, DrzavaAdmin)
admin.site.register(Grad, GradAdmin)
admin.site.register(Objekat)
admin.site.register(DeoGrada)
admin.site.register(Namestenost)
admin.site.register(TipObjekta)
