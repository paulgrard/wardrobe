from django.shortcuts import render
from django.http import HttpResponse
from dressingManage.forms import AddClothesForm, forms
from django.contrib.auth.models import User
from dressingManage.models import Clothes, Categories
import json

# Create your views here.

def accueil(request):
    return render(request, 'dressingManage/accueil.html')


def addClothe(request):
    data = []
    if request.method == "POST":
        form = AddClothesForm(request.POST, user=request.user)
        if form.is_valid():
            warmthC = form.cleaned_data["warmth"]
            photoC = form.cleaned_data["photo"]
            categorieC = Categories.objects.get(name = form.cleaned_data["categorie"])
            themeC = form.cleaned_data["theme"]
            colorC = form.cleaned_data["color"]

            if request.user:
                currentUser = request.user
                newClothe = Clothes.objects.create(warmth = warmthC, photo = photoC, state = 0, nbreUse = 0, categorie = categorieC, theme = themeC, user = currentUser, color = colorC)
                if newClothe:
                    data = {'new_clothe':newClothe.photo}
                else:
                    data = {'new_clothe':'Error during creation of clothe'}
            else:
                data = {'new_clothe':'User is not authenticate'}
    else:
        form = AddClothesForm(user=request.user)

    return render(request, 'dressingManage/addClothe.html', locals())
    return HttpResponse(json.dumps(data), content_type='application/json')
