from django.contrib import admin
from nekretnine.models import Drzava, Grad, Objekat, ObjectImage, DeoGrada, Namestenost, TipObjekta, Heating

class GradInline(admin.TabularInline):
	model = Grad

class DrzavaAdmin(admin.ModelAdmin):
	inlines = [GradInline]
	
class DeoGradaInline(admin.TabularInline):	
	model = DeoGrada

class GradAdmin(admin.ModelAdmin):
	inlines = [DeoGradaInline]

class ObjectImageInline(admin.TabularInline):
    model = ObjectImage

class ObjectAdmin(admin.ModelAdmin):
	inlines = [ObjectImageInline]

admin.site.register(Drzava, DrzavaAdmin)
admin.site.register(Grad, GradAdmin)
admin.site.register(Objekat, ObjectAdmin)
admin.site.register(DeoGrada)
admin.site.register(Namestenost)
admin.site.register(TipObjekta)
admin.site.register(Heating)
