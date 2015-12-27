from django.shortcuts import render
from django.http import HttpResponse
from dressingManage.forms import AddClotheForm, forms
from django.contrib.auth.models import User
from dressingManage.models import Clothe, Categorie, Color
import json

# Create your views here.

def accueil(request):
    return render(request, 'dressingManage/accueil.html')


def addClothe(request):
    data = []
    if request.method == "POST":
        form = AddClotheForm(request.POST, user=request.user)
        if form.is_valid():
            warmthC = form.cleaned_data["warmth"]
            photoC = form.cleaned_data["photo"]
            categorieC = Categorie.objects.get(name = form.cleaned_data["categorie"], area = form.cleaned_data["area"])
            themesC = form.cleaned_data["themes"]
            colorsC = form.cleaned_data["color"]

            if request.user:
                currentUser = request.user
                newClothe = Clothe.objects.create(warmth = warmthC, photo = photoC, state = 0, nbreUse = 0, categorie = categorieC, user = currentUser)
                if themesC:
                    newClothe.themes.add(themesC)
                #for valColor in colorsC:
                col = Color.objects.create(color = str(colorsC))#color = valColor
                newClothe.colors.add(col)
                
                if newClothe:
                    data = {'new_clothe':newClothe.photo}
                else:
                    data = {'new_clothe':'Error during creation of clothe'}
            else:
                data = {'new_clothe':'User is not authenticate'}
    else:
        form = AddClotheForm(user=request.user)

    return render(request, 'dressingManage/addClothe.html', locals())
    return HttpResponse(json.dumps(data), content_type='application/json')
