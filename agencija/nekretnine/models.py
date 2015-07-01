import os
from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def validate_positive_number(value):
	if value <= 0:
		raise ValidationError("{0} is not positive number")

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

class AdditionalFeatures(models.Model):
	name = models.TextField()
	def __str__(self):
		return self.name

class Owner(models.Model):
	user = models.ForeignKey(User)
	phone = models.BigIntegerField(validators=[validate_positive_number])
	def __str__(self):
		return "{0} {1}".format(self.user.first_name, self.user.last_name)

class Objekat(models.Model):
	adresa = models.TextField()
	tip_objekta = models.ForeignKey(TipObjekta)
	deo_grada = models.ForeignKey(DeoGrada)
	broj_soba = models.FloatField()
	povrsina = models.IntegerField()
	cena = models.IntegerField()
	deposit = models.IntegerField()
	construction_year = models.IntegerField()
	free_message = models.TextField()
	namestenost = models.ForeignKey(Namestenost)
	additional_features = models.ManyToManyField(AdditionalFeatures)
	floor = models.IntegerField()
	floors = models.IntegerField()
	heating = models.ForeignKey(Heating)
	owner = models.ForeignKey(Owner)
	
	@property
	def images(self):
		result = []
		for object_image in self.objectimage_set.all():
			extension = os.path.splitext(object_image.image.path)[1]
			result.append({'large_image': object_image.image, 'small_url': object_image.image.url + '.small' + extension})
		return result

	@property
	def thumb(self):
		img = self.objectimage_set.first().image
		extension = os.path.splitext(img.path)[1]
		return img.url + '.small' + extension

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
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)
	reported_as_inactive_counter = models.IntegerField(default = 0)
	
	def __str__(self):
		return "{0}, active: {1}, reported inactive: {2} times".format(self.object, self.active, self.reported_as_inactive_counter)
	
	class Meta:
		ordering = ['-active', '-reported_as_inactive_counter']

class AdReporter(models.Model):
	ad = models.ForeignKey(Ad)
	reporter_token = models.IntegerField()
	reporter_ip_address = models.TextField()
