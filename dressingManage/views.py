from django.shortcuts import render
from django.http import HttpResponse
from dressingManage.forms import AddClotheForm, forms
from django.contrib.auth.models import User
from dressingManage.models import Clothe, Categorie, Color, Theme
import json

# Create your views here.

def accueil(request):
    return render(request, 'dressingManage/accueil.html')

#penser à renommer les photos et faire une requete avant d'ajouter la photo pour savoir si elle est unique ou non
#plus voir au niveau BDD le coup de area dans categorie
#pour l'instant on ne peut passer qu'un theme et qu'une couleur
def addClothe(request):
    data = []
    themes = []
    currentUser = request.user
    if request.method == "POST":
        form = AddClotheForm(request.POST, user=request.user)
        if form.is_valid():
            warmthC = form.cleaned_data["warmth"]
            photoC = form.cleaned_data["photo"]
            categorieC = Categorie.objects.get(name = form.cleaned_data["categorie"], area = form.cleaned_data["area"])
            themesC = form.cleaned_data["themes"]
            colorsC = form.cleaned_data["color"]

            if currentUser:
                newClothe = Clothe(warmth = warmthC, photo = photoC, state = 0, nbreUse = 0, categorie = categorieC, user = currentUser)
                newClothe.save()
                if themesC:
                    newClothe.themes.add(themesC)
                
                #for valColor in colorsC:
                if colorsC:
                    col = Color(color = colorsC)#color = valColor
                    col.save()
                    newClothe.colors.add(col)
                
                '''yolo=newClothe.colors.all()
                for x in yolo:
                    yolo2 = x.color
                data = {'new_clothe':yolo2}
                return HttpResponse(json.dumps(data), content_type='application/json')'''
                
                if newClothe:
                    data = {'new_clothe':newClothe.photo}
                else:
                    data = {'new_clothe':'Error during creation of clothe'}
            else:
                data = {'new_clothe':'User is not authenticate'}

            return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        #form = AddClotheForm(user=request.user)
        themesFromUser = Theme.objects.filter(userOwner = currentUser)
        for theme in themesFromUser:
            themes.append(theme.name)
        data = {'themes':themes}
        

    #return render(request, 'dressingManage/addClothe.html', locals())
    return HttpResponse(json.dumps(data), content_type='application/json')
