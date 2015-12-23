from django.shortcuts import render, redirect
from connexion.forms import ConnexionForm

from django.http import HttpResponse
# Create your views here.

from django.http import Http404

from django.contrib.auth import authenticate, login

def connexion(request):
    error = False

    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
            else: # sinon une erreur sera affichée
                error = True
    else:
        form = ConnexionForm()

    return render(request, 'connexion/connexion.html', locals())




from django.contrib.auth import logout
from django.core.urlresolvers import reverse

def deconnexion(request):
    logout(request)
    return redirect(reverse(connexion))

'''from django.contrib.auth.decorators import login_required

@login_required
def dire_bonjour(request):
    if request.user.is_authenticated():
        return HttpResponse("Salut, {0} !".format(request.user.username))
    return HttpResponse("Salut, anonyme.")'''

