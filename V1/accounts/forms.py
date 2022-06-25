from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

User = get_user_model()

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Adresse mail', required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Entrez votre adresse mail...'}))
    password = forms.CharField(label='Mot de passe', required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Entrez votre mot de passe...'}))

class UserForm(UserCreationForm):
    first_name = forms.CharField(label='Prénom', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Entrez votre prénom...'}))
    last_name = forms.CharField(label='Nom', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Entrez votre nom de famille...'}))
    email = forms.CharField(label='Adresse mail', required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Entrez votre adresse mail...'}))
    password1 = forms.CharField(label='Mot de passe', required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Entrez votre mot de passe...'}))
    password2 = forms.CharField(label='Vérification du mot de passe', required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Confirmez votre mot de passe...'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')
