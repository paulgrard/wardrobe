# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth import login, logout
from userManage.forms import AddForm, forms
from django.contrib.auth.models import User
from userManage.models import Parameters

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
            sexType = form.cleaned_data["sex"]
            if User.objects.filter(email=new_mail).exists() or User.objects.filter(username=new_username).exists():
                data['message'] = 'Ce mail ou ce pseudo est déja utilisé.'
            else:
                newUser = User.objects.create_user(username=new_username, email=new_mail, password=new_password)
                newParam = Parameters(user = newUser, sex = sexType)
                newParam.save()
                if newUser:
                    success = True
                else:
                    data['message'] = 'Erreur lors de la création de l\'utilisateur.'
                    
        else: #si form non valide
            data['message'] = 'Formulaire non valide.'
            
    else: #si non requete POST
        form = AddForm()
        data['message'] = 'Une requête POST est nécessaire.'

    data['success'] = success
    return render(request, 'userManage/add.html', locals())
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


def setSex(request, sexType):
    data={}
    success = False

    if request.user.is_authenticated():
        param = get_object_or_404(Parameters, user = request.user)
        param.sex = sexType
        param.save()
        success = True
    else:
        return HttpResponseForbidden('Utilisateur non authentifié')

    data['success'] = success
    return HttpResponse(json.dumps(data), content_type='application/json')
