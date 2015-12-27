from django import forms

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from dressingManage.models import Theme

class AddClotheForm(forms.Form):
        
    def __init__(self, *args, **kwargs):
        currentUser = kwargs.pop('user')
        super(AddClotheForm, self).__init__(*args, **kwargs)
        
        self.fields['themes'].queryset = Theme.objects.filter(userOwner = currentUser) 

        
    warmth = forms.IntegerField(label="Chaleur du vêtement")
    photo = forms.CharField(label = "Image du vêtement")
    area = forms.CharField(label = "Zone du vêtement")
    categorie = forms.IntegerField(label = "Catégorie du vêtement")
    themes = forms.ModelChoiceField(queryset=None, required=False, label = "Thèmes du vêtement")
    color = forms.CharField(label = "Couleurs du vêtement", max_length=7)
