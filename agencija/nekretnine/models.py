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
	phone = models.BigIntegerField(validators=[validate_positive_number], null=True)
	show_data_in_ad = models.BooleanField(default=True)

	@property
	def objects_count(self):
		return self.objekat_set.count()

	def __str__(self):
		return "{0} {1} (objekata: {2})".format(self.user.first_name, self.user.last_name, self.objects_count)

class Objekat(models.Model):
	adresa = models.TextField()
	tip_objekta = models.ForeignKey(TipObjekta)
	deo_grada = models.ForeignKey(DeoGrada)
	broj_soba = models.FloatField()
	povrsina = models.IntegerField()
	cena = models.IntegerField()
	deposit = models.BooleanField()
	construction_year = models.IntegerField(null=True, blank=True)
	free_message = models.TextField(blank=True)
	namestenost = models.ForeignKey(Namestenost)
	additional_features = models.ManyToManyField(AdditionalFeatures, blank=True)
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
	def get_additional_features(self):
		feature_names = [feature.name for feature in self.additional_features.all()]
		return ", ".join(feature_names) if len(feature_names) > 0 else "-"

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
	reported_as_middleman_counter = models.IntegerField(default = 0)

	def __str__(self):
		return "{0}, active: {1}, prijavljen kao izdat: {2} puta, prijavljen posrednik: {3} puta".\
			format(self.object, self.active, self.reported_as_inactive_counter, self.reported_as_middleman_counter)
	
	class Meta:
		ordering = ['-active', '-reported_as_inactive_counter']

class AdReporter(models.Model):
	ad = models.ForeignKey(Ad)
	reporter_token = models.IntegerField()
	reporter_ip_address = models.TextField()

class UserMessage(models.Model):
	object = models.ForeignKey(Objekat)
	message = models.TextField()
	sender_token = models.IntegerField()
	sender_ip_address = models.TextField()

	def __str__(self):
		return "owner: {0}, message: {1}".\
			format(self.object.owner, self.message[:30] + '...')
