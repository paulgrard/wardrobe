# -*- coding: utf-8 -*-
from django import forms


class AddForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    mail = forms.EmailField(label = "Mail d'utilisateur")
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
