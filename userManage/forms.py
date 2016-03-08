# -*- coding: utf-8 -*-
from django import forms
from django.core.validators import MaxValueValidator

class AddForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    mail = forms.EmailField(label = "Mail d'utilisateur")
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    sex = forms.IntegerField(label="Sexe", validators=[MaxValueValidator(2)])

class setParamForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30, required=False)
    mail = forms.EmailField(label = "Mail d'utilisateur", required=False)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput, required=False)
    sex = forms.IntegerField(label="Sexe", validators=[MaxValueValidator(2)], required=False)
