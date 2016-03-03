# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth import login, logout
from userManage.forms import AddForm, forms
from django.contrib.auth.models import User
import json


def add(request):
    data = {}
    success = False

    if request.method == "POST":
        form = AddForm(request.POST)
        if form.is_valid():
            new_username = form.cleaned_data["username"]
            new_mail = form.cleaned_data["mail"]
            new_password = form.cleaned_data["password"]
            if User.objects.filter(email=new_mail).exists() or User.objects.filter(username=new_username).exists():
                data['message'] = 'Ce mail ou ce pseudo est déja utilisé.'
            else:
                user = User.objects.create_user(username=new_username, email=new_mail, password=new_password)
                if user:
                    success = True
                else:
                    data['message'] = 'Erreur lors de la création de l\'utilisateur.'

        else: #si form non valide
            data['message'] = 'Formulaire non valide.'

    else: #si non requete POST
        form = AddForm()
        data['message'] = 'Une requête POST est nécessaire.'

    data['success'] = success
    return HttpResponse(json.dumps(data), content_type='application/json')



def deactivate(request):
    data = {}
    success = False

    if request.user.is_authenticated():
        userToDeactivate = request.user
        if userToDeactivate.is_active:
            userToDeactivate.is_active=False
            userToDeactivate.save()
            success = True
            logout(request)
        else:
            data['message'] = 'Utilisateur déjà désactivé.'
    else:
        return HttpResponseForbidden('Utilisateur non authentifié')

    data['success'] = success
    return HttpResponse(json.dumps(data), content_type='application/json')
