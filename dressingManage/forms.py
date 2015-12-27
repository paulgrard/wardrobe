from django import forms

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from dressingManage.models import Themes

class AddClothesForm(forms.Form):
        
    def __init__(self, *args, **kwargs):
        currentUser = kwargs.pop('user')
        super(AddClothesForm, self).__init__(*args, **kwargs)
        
        self.fields['theme'].queryset = Themes.objects.filter(userOwner = currentUser) 

        
    warmth = forms.IntegerField(label="Chaleur du vêtement")
    photo = forms.CharField(label = "Image du vêtement")
    categorie = forms.IntegerField(label = "Catégorie du vêtement")
    theme = forms.ModelChoiceField(queryset=None, required=False, label = "Thèmes du vêtement")
    color = forms.CharField(label = "Couleurs du vêtement", max_length=7)
