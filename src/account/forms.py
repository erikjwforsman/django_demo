from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from account.models import Account


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60,help_text="Vaadittu")

    class Meta:
        model = Account
        fields = ("first_name", "last_name", "email", "username", "password1", "password2")

class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ("username", "password")

    def clean(self):
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]
        if not authenticate(username=username, password=password):
            raise forms.ValidationError("Hups, käyttäjänimi tai salasana prakaa")


class AccountUpdateForm(forms.ModelForm):

    class Meta:
        model=Account
        fields=("first_name", "last_name", "username", "email", "motto", "image")

    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data["username"]
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
            except Account.DoesNotExist:
                return username
            raise forms.ValidationError(f"Käyttäjänimi {username} on jo käytössä") #Ehkä account.username->{} ja alas

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data["email"]
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
            except Account.DoesNotExist:
                return email
            raise forms.ValidationError(f"Sähköpostiosoite {email} on jo käytössä")
