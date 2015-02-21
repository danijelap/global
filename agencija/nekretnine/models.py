from django.db import models

# Create your models here.
class Drzava(models.Model):
	name = models.CharField(max_length=50)
	def __str__(self):
		return self.name
	@property
	def gradovi(self):
		return self.grad_set.all()

class Grad(models.Model):
	name = models.CharField(max_length=50)
	drzava = models.ForeignKey(Drzava)
	def __str__(self):
		return self.name
	@property
	def delovi_grada(self):
		return self.deograda_set.all()

class DeoGrada(models.Model):
	name = models.CharField(max_length=50)
	grad = models.ForeignKey(Grad)
	def __str__(self):
		return self.name

class TipObjekta(models.Model):
	name = models.TextField()
	def __str__(self):
		return self.name

class Namestenost(models.Model):
	name = models.TextField()
	def __str__(self):
		return self.name

class Heating(models.Model):
	name = models.TextField()
	def __str__(self):
		return self.name

class Objekat(models.Model):
	adresa = models.TextField()
	tip_objekta = models.ForeignKey(TipObjekta)
	deo_grada = models.ForeignKey(DeoGrada)
	broj_soba = models.FloatField()
	povrsina = models.IntegerField()
	cena = models.IntegerField()
	namestenost = models.ForeignKey(Namestenost)
	has_terrace = models.BooleanField(default=False)
	has_air_conditioner = models.BooleanField(default=False)
	has_cable = models.BooleanField(default=False)
	has_elevator = models.BooleanField(default=False)
	floor = models.IntegerField()
	floors = models.IntegerField()
	heating = models.ForeignKey(Heating)
	
	@property
	def images(self):
		result = []
		for object_image in self.objectimage_set.all():
			result.append(object_image.image)
		return result
	def __str__(self):
		return self.adresa

class ObjectImage(models.Model):
	def upload_path(self, filename):
		return "objects/%s/%s" % (str(self.object.id), filename)
	object = models.ForeignKey(Objekat)
	image = models.ImageField(upload_to=upload_path)