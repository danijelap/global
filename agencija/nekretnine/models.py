import os
from PIL import Image
from django.db import models
from django.core.validators import validate_email

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

class Owner(models.Model):
	name = models.TextField()
	email = models.TextField(validators = [validate_email])
	phone = models.TextField()
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
	owner = models.ForeignKey(Owner)
	
	@property
	def images(self):
		result = []
		for object_image in self.objectimage_set.all():
			extension = os.path.splitext(object_image.image.path)[1]
			result.append({'large_image': object_image.image, 'small_url': object_image.image.url + 'small' + extension})
		return result
	def __str__(self):
		return "{0} ({1} m2, {2} €)".format(self.deo_grada.name, self.povrsina, self.cena)

class ObjectImage(models.Model):
	def upload_path(self, filename):
		return "objects/%s/%s" % (str(self.object.id), filename)
	
	object = models.ForeignKey(Objekat)
	image = models.ImageField(upload_to=upload_path)
	
	def save(self, *args, **kwargs):
		if self.image:
			super(ObjectImage, self).save()
			new_image = Image.open(self.image)
			new_size = (800, 450)
			new_image.resize(new_size).save(self.image.path)
			extension = os.path.splitext(self.image.path)[1]
			thumb_size = (80, 45)
			new_image.resize(thumb_size).save(self.image.path + '.small' + extension)

class Ad(models.Model):
	object = models.ForeignKey(Objekat)
	created_at = models.DateTimeField()
	updated_at = models.DateTimeField()
	active = models.BooleanField(default=True)
	reported_as_inactive_counter = models.IntegerField(default = 0)
	
	def __str__(self):
		return self.object.__str__()

class AdReporter(models.Model):
	ad = models.ForeignKey(Ad)
	reporter_token = models.IntegerField()
	reporter_ip_address = models.TextField()
