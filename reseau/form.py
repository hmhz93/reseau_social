from django import forms
from django.contrib.auth.models import User
from .models import *


class AuthenticationForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)


class CreationForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    verify_password = forms.CharField(label="Vérification du mot de passe", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(CreationForm, self).clean()
        password = cleaned_data.get('password')
        verify_password = cleaned_data.get('verify_password')

        if password != verify_password:
            self.add_error("password", "password non identique")
        return cleaned_data


class CommentaireForm(forms.Form):
    texte = forms.CharField(label="Commentaire")
    commentaire_parent = forms.CharField(widget=forms.HiddenInput)
