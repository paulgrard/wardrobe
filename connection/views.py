# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from connection.forms import ConnectionForm
from django.http import HttpResponse, HttpResponseForbidden
from django.http import Http404
from django.contrib.auth import authenticate, login
import json


def connection(request):
    success = False
    data = {}

    if request.method == "POST":
        form = ConnectionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
            if user and user.is_active:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
                success = True
        else:
            data['message'] = 'Formulaire non valide.'
        data['success'] = success
    else:
        if request.user.is_authenticated():
            data['message'] = 'Utilisateur déjà connecté.'
            data['success'] = success
            return HttpResponse(json.dumps(data), content_type='application/json')
        form = ConnectionForm()

    return render(request, 'connection/connection.html', locals())
    return HttpResponse(json.dumps(data), content_type='application/json')

def getToken(request):
    return render(request, 'connection/getToken.html', locals())

from django.contrib.auth import logout
from django.core.urlresolvers import reverse

def deconnection(request):
    if request.user.is_authenticated():
        logout(request)
        data= {'success':'True'}

        return HttpResponse(json.dumps(data), content_type='application/json')
        #return redirect(reverse(connection))

    return HttpResponseForbidden('Utilisateur non authentifié')

'''from django.contrib.auth.decorators import login_required

@login_required
def dire_bonjour(request):
    if request.user.is_authenticated():
        return HttpResponse("Salut, {0} !".format(request.user.username))
    return HttpResponse("Salut, anonyme.")'''

