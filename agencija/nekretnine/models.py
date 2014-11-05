from django.db import models

# Create your models here.
class Drzava(models.Model):
	naziv = models.CharField(max_length=50)
	def __str__(self):
		return self.naziv
	@property
	def gradovi(self):
		return self.grad_set.all()

class Grad(models.Model):
	naziv = models.CharField(max_length=50)
	drzava = models.ForeignKey(Drzava)
	def __str__(self):
		return self.naziv

class DeoGrada(models.Model):
	naziv = models.CharField(max_length=50)
	grad = models.ForeignKey(Grad)
	def __str__(self):
		return self.naziv

class TipObjekta(models.Model):
	naziv = models.TextField()
	def __str__(self):
		return self.naziv

class Namestenost(models.Model):
	naziv = models.TextField()
	def __str__(self):
		return self.naziv

class Objekat(models.Model):
	adresa = models.TextField()
	tip_objekta = models.ForeignKey(TipObjekta)
	deo_grada = models.ForeignKey(DeoGrada)
	broj_soba = models.FloatField()
	povrsina = models.IntegerField()
	cena = models.IntegerField()
	namestenost = models.ForeignKey(Namestenost)
	def __str__(self):
		return self.adresa
