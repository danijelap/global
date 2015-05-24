from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.utils.translation import ugettext_lazy as _
from nekretnine.models import *

class UserRegistrationForm(forms.Form):
	
	error_messages = {
		'password_mismatch': _("Lozinke se ne poklapaju."),
		'user_exists': _("Postoji nalog sa ovom email adresom.")
	}
	
	email = forms.EmailField(label = _("Email adresa"))
	password1 = forms.CharField(label = _("Lozinka"),
		widget=forms.PasswordInput)
	password2 = forms.CharField(label = _("Ponovite lozinku"),
		widget=forms.PasswordInput,
		help_text = _("Unesite istu lozinku ponovo, zbog potvrde."))
	first_name = forms.CharField(label=_("Ime"))
	last_name = forms.CharField(label=_("Prezime"))
	
	def clean_email(self):
		email = self.cleaned_data.get("email")
		if len(User.objects.filter(username = email)) > 0:
			raise forms.ValidationError(
				self.error_messages['user_exists'],
				code='user_exists',
			)
		return email
	
	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError(
				self.error_messages['password_mismatch'],
				code='password_mismatch',
			)
		return password2
	
	
	def save(self, commit=True):
		# create user model which will have additional fields
		# create user model for unconfirmed accounts
		user = User.objects.create_user(
			username = self.cleaned_data["email"],
			password = self.cleaned_data["password1"],
			email = self.cleaned_data["email"],
			first_name = self.cleaned_data["first_name"],
			last_name = self.cleaned_data["last_name"]
		)
		user.is_active = False
		owner = Owner(user = user)
		if commit:
			user.save()
			owner.save()
		return (user, owner)

class UserLoginForm(forms.Form):
	error_messages = {
		'wrong_user_name_or_password': _("Pogrešna email adresa ili lozinka!"),
		'account_disabled': _("Vaš nalog nije aktiviran. Proverite email i ispratite uputstva."),
	}
	email = forms.EmailField(label = _("Email adresa"))
	password = forms.CharField(label = _("Lozinka"),
		widget=forms.PasswordInput)

	def clean_password(self):
		email = self.cleaned_data.get("email")
		password = self.cleaned_data.get("password")
		if len(User.objects.filter(username=email, password=password)) == 1:
			# User is valid, active and authenticated
			return password
		else:
			raise forms.ValidationError(
				self.error_messages['wrong_user_name_or_password'],
				code='wrong_user_name_or_password',
			)
	
	def login(self, request):
		email = self.cleaned_data.get("email")
		password = self.cleaned_data.get("password")
		user = authenticate(username = email, password = password)
		if user is not None:
			if user.is_active():
				auth_login(request, user)
			else:
				raise forms.ValidationError(
					self.error_messages['account_disabled'],
					code='account_disabled',
				)
		else:
			raise forms.ValidationError(
				self.error_messages['wrong_user_name_or_password'],
				code='wrong_user_name_or_password',
			)
		return user

class ObjectForm(forms.ModelForm):
	error_messages = {
		'account_disabled': _("Vaš nalog nije aktiviran. Proverite email i ispratite uputstva."),
	}
	
	class Meta:
		model = Objekat
		fields = [ 'adresa', 'tip_objekta', 'deo_grada', 'broj_soba', 'povrsina', 
			'cena', 'namestenost', 'has_terrace', 'has_air_conditioner', 'has_cable', 
			'has_elevator', 'floor', 'floors', 'heating' ]
		labels = {
			'adresa': _("Adresa"),
			'tip_objekta': _("Tip objekta"),
			'deo_grada': _("Deo grada"),
			'broj_soba': _("Broj soba"),
			'povrsina': _("Površina"),
			'cena': _("Cena"),
			'namestenost': _("Nameštenost"),
			'has_terrace': _("Terasa"),
			'has_air_conditioner': _("Klima uređaj"),
			'has_cable': _("Kablovska TV"),
			'has_elevator': _("Lift"),
			'floor': _("Sprat"),
			'floors': _("Spratnost zgrade"),
			'heating': _("Grejanje"),
		}

class ObjectImageForm(forms.ModelForm):
	class Meta:
		model = ObjectImage
		fields = ['image']
		labels = {
			'image': 'Slika',
		}

class AdForm(forms.ModelForm):
	class Meta:
		model = Ad
		fields = ['active']
		labels = {
			'active': 'Aktivan',
		}

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['email', 'first_name', 'last_name']
		labels = {
			'email': _("Email adresa"),
			'first_name': _("Ime"),
			'last_name': _("Prezime"),
		}

class OwnerForm(forms.ModelForm):
	class Meta:
		model = Owner
		fields = ['phone']
		labels = {
			'phone': _("Telefon"),
		}
		widgets = {
			'phone': forms.TextInput(attrs={'size': 15, 'title': _("Broj telefona")}),
		}

class ChangePasswordForm(forms.Form):

	error_messages = {
		'password_mismatch': _("Lozinke se ne poklapaju."),
	}

	old_password = forms.CharField(label = _("Stara lozinka"),
		widget=forms.PasswordInput)
	new_password1 = forms.CharField(label = _("Nova lozinka"),
		widget=forms.PasswordInput)
	new_password2 = forms.CharField(label = _("Ponovite lozinku"),
		widget=forms.PasswordInput)

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super(ChangePasswordForm, self).__init__(*args, **kwargs)

	def clean(self):
		old_password = self.cleaned_data.get("old_password")
		new_password1 = self.cleaned_data.get("new_password1")
		new_password2 = self.cleaned_data.get("new_password2")
		if not (old_password and self.user and
				self.user.check_password(old_password) and
				new_password1 and new_password2 and
				new_password1 == new_password2):
			raise forms.ValidationError(
				self.error_messages['password_mismatch'],
				code='password_mismatch',
			)

	def save(self):
		self.user.set_password(self.cleaned_data['new_password1'])
		self.user.save()

