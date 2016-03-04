# -*- coding: utf-8 -*-
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from dressingManage.models import Theme
from django.core.exceptions import ValidationError


    
class AddClotheForm(forms.Form):
        
   
    def validate_file_extension(value):
        ext = [".jpg", ".JPG", ".jpeg", ".JPEG"]
        if not value.name.endswith(tuple(ext)):
            raise ValidationError('Le type de fichier n\'est pas pris en charge')
        
        
    warmth = forms.IntegerField(label="Chaleur du vêtement")
    photo = forms.FileField(label = "Image du vêtement", validators=[validate_file_extension])
    area = forms.CharField(label = "Zone du vêtement")
    category = forms.IntegerField(label = "Catégorie du vêtement")
    themes = forms.CharField(label = "Ids des thèmes du vêtement")
    #themes = forms.ModelChoiceField(queryset=None, required=False, widget=FilteredSelectMultiple("Thèmes du vêt", is_stacked=False), label = "Thèmes du vêtement")
    color1 = forms.CharField(label = "Couleur 1 du vêtement", max_length=7, min_length=7)
    quantity1 = forms.IntegerField(label = "Pourcentage 1 de la couleur")
    
    color2 = forms.CharField(label = "Couleur 2 du vêtement", max_length=7, min_length=7, required=False)
    quantity2 = forms.IntegerField(label = "Pourcentage 2 de la couleur", required=False)
    
    color3 = forms.CharField(label = "Couleur 3 du vêtement", max_length=7, min_length=7, required=False)
    quantity3 = forms.IntegerField(label = "Pourcentage 3 de la couleur", required=False)



class EditClotheForm(forms.Form):

    def validate_file_extension(value):
        ext = [".jpg", ".JPG", ".jpeg", ".JPEG"]
        if not value.name.endswith(tuple(ext)):
            raise ValidationError('Le type de fichier n\'est pas pris en charge')
        
    warmth = forms.IntegerField(label="Chaleur du vêtement", required=False)
    photo = forms.FileField(label = "Image du vêtement", validators=[validate_file_extension], required=False)
    area = forms.CharField(label = "Zone du vêtement", required=False)
    category = forms.IntegerField(label = "Catégorie du vêtement", required=False)
    themes = forms.CharField(label = "Ids des thèmes du vêtement", required=False)
    color1 = forms.CharField(label = "Couleur 1 du vêtement", max_length=7, min_length=7, required=False)
    quantity1 = forms.IntegerField(label = "Pourcentage 1 de la couleur", required=False)

    color2 = forms.CharField(label = "Couleur 2 du vêtement", max_length=7, min_length=7, required=False)
    quantity2 = forms.IntegerField(label = "Pourcentage 2 de la couleur", required=False)

    color3 = forms.CharField(label = "Couleur 3 du vêtement", max_length=7, min_length=7, required=False)
    quantity3 = forms.IntegerField(label = "Pourcentage 3 de la couleur", required=False)


class AddThemeForm(forms.Form):
        
    name = forms.CharField(label = "Nom du thème", max_length=30)
    
class GetThemeForm(forms.Form):
        
    name = forms.CharField(label = "Nom du thème", max_length=30)


class WeatherForm(forms.Form):
        
    lat = forms.CharField(label = "lat", max_length=20)
    lon = forms.CharField(label = "lon", max_length=20)
