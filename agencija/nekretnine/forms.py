from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
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
			username=self.cleaned_data["email"],
			password=self.cleaned_data["password1"],
			email=self.cleaned_data["email"],
			first_name=self.cleaned_data["first_name"],
			last_name=self.cleaned_data["last_name"]
		)
		# user.is_active = False
		owner = Owner(user=user)
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
		fields = ['adresa', 'tip_objekta', 'deo_grada', 'broj_soba', 'povrsina',
			'cena', 'construction_year', 'namestenost', 'additional_features', 'floor', 'floors',
			'heating', 'deposit', 'free_message']
		labels = {
			'adresa': _("Adresa"),
			'tip_objekta': _("Tip objekta"),
			'deo_grada': _("Deo grada"),
			'broj_soba': _("Broj soba"),
			'povrsina': mark_safe("Površina (m<sup>2</sup>)"),
			'cena': _("Cena (€)"),
			'construction_year': _("Godina izgradnje"),
			'namestenost': _("Nameštenost"),
			'additional_features': _("Ostale pogodnosti"),
			'floor': _("Sprat"),
			'floors': _("Spratnost zgrade"),
			'heating': _("Grejanje"),
			'deposit': _("Depozit"),
			'free_message': _("Slobodna poruka"),
		}

# hack because bug in Django https://code.djangoproject.com/ticket/9321
ObjectForm.base_fields['additional_features'].help_text = "Držite Ctrl dugme (Command na Mac-u) da biste izabrali više opcija"

class NewImagesForm(forms.Form):

	image1 = forms.ImageField(required=False, label=_("Dodajte sliku"))
	image2 = forms.ImageField(required=False, label=_("Dodajte sliku"))
	image3 = forms.ImageField(required=False, label=_("Dodajte sliku"))
	image4 = forms.ImageField(required=False, label=_("Dodajte sliku"))
	image5 = forms.ImageField(required=False, label=_("Dodajte sliku"))
	image6 = forms.ImageField(required=False, label=_("Dodajte sliku"))
	image7 = forms.ImageField(required=False, label=_("Dodajte sliku"))
	image8 = forms.ImageField(required=False, label=_("Dodajte sliku"))
	image9 = forms.ImageField(required=False, label=_("Dodajte sliku"))
	image10 = forms.ImageField(required=False, label=_("Dodajte sliku"))

	def get_images(self):
		images = []
		image1 = self.cleaned_data.get("image1")
		if image1: images.append(ObjectImage(image=image1))
		image2 = self.cleaned_data.get("image2")
		if image2: images.append(ObjectImage(image=image2))
		image3 = self.cleaned_data.get("image3")
		if image3: images.append(ObjectImage(image=image3))
		image4 = self.cleaned_data.get("image4")
		if image4: images.append(ObjectImage(image=image4))
		image5 = self.cleaned_data.get("image5")
		if image5: images.append(ObjectImage(image=image5))
		image6 = self.cleaned_data.get("image6")
		if image6: images.append(ObjectImage(image=image6))
		image7 = self.cleaned_data.get("image7")
		if image7: images.append(ObjectImage(image=image7))
		image8 = self.cleaned_data.get("image8")
		if image8: images.append(ObjectImage(image=image8))
		image9 = self.cleaned_data.get("image9")
		if image9: images.append(ObjectImage(image=image9))
		image10 = self.cleaned_data.get("image10")
		if image10: images.append(ObjectImage(image=image10))
		return images

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
		fields = ['first_name', 'last_name']
		labels = {
			'first_name': _("Ime"),
			'last_name': _("Prezime"),
		}

class OwnerForm(forms.ModelForm):
	class Meta:
		model = Owner
		fields = ['phone', 'show_data_in_ad']
		labels = {
			'phone': _("Telefon"),
			'show_data_in_ad': _("Prikaži lične podatke u oglasima"),
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

