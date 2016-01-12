from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from dressingManage.models import Theme

class AddClotheForm(forms.Form):
        
    def __init__(self, *args, **kwargs):
        currentUser = kwargs.pop('user')
        super(AddClotheForm, self).__init__(*args, **kwargs)
        
        self.fields['themes'].queryset = Theme.objects.filter(userOwner = currentUser) 
        #self.fields['themes']=forms.ModelChoiceField(queryset = Theme.objects.filter(userOwner = currentUser) , required=False, widget=FilteredSelectMultiple("Thèmes du vêt", is_stacked=False), label = "Thèmes du vêtement")

        
    warmth = forms.IntegerField(label="Chaleur du vêtement")
    photo = forms.CharField(label = "Image du vêtement")
    area = forms.CharField(label = "Zone du vêtement")
    category = forms.IntegerField(label = "Catégorie du vêtement")
    themes = forms.ModelChoiceField(queryset=None, required=False, widget=FilteredSelectMultiple("Thèmes du vêt", is_stacked=False), label = "Thèmes du vêtement")
    color = forms.CharField(label = "Couleurs du vêtement", max_length=7)


class AddThemeForm(forms.Form):
        
        name = forms.CharField(label = "Nom du thème", max_length=30)
