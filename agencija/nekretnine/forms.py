from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from nekretnine.models import Owner

class UserRegistrationForm(forms.Form):
	
	error_messages = {
		'password_mismatch': "Lozinke se ne poklapaju.",
		'user_exists': 'Postoji nalog sa ovom email adresom.'
	}
	
	email = forms.EmailField(label = "Email adresa")
	password1 = forms.CharField(label = "Lozinka",
		widget=forms.PasswordInput)
	password2 = forms.CharField(label = "Ponovite lozinku",
		widget=forms.PasswordInput,
		help_text = "Unesite istu lozinku ponovo, zbog potvrde.")
	first_name = forms.CharField(label = "Ime")
	last_name = forms.CharField(label = "Prezime")
	
	def clean_email(self):
		email = self.cleaned_data.get("email")
		if len(User.objects.filter(username = email)) > 0:
			raise forms.ValidationError(
				self.error_messages['user_exists'],
				code='user_exists',
			)
		return username
	
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
		'wrong_user_name_or_password': "Pogrešna email adresa ili lozinka!",
		'account_disabled': "Vaš nalog nije aktiviran. Proverite email i ispratite uputstva.",
	}
	email = forms.EmailField(label = "Email adresa")
	password = forms.CharField(label = "Lozinka",
		widget=forms.PasswordInput)

	def clean_password(self):
		email = self.cleaned_data.get("email")
		password = self.cleaned_data.get("password")
		user = authenticate(username = email, password = password)
		if user is not None:
			if user.is_active:
				# User is valid, active and authenticated
				return user
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
