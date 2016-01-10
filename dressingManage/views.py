from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from dressingManage.forms import AddClotheForm, forms
from django.contrib.auth.models import User
from dressingManage.models import Clothe, Category, Color, Theme
import json

# Create your views here.

def accueil(request):
    return render(request, 'dressingManage/accueil.html')

#penser à renommer les photos et faire une requete avant d'ajouter la photo pour savoir si elle est unique ou non
#plus voir au niveau BDD le coup de area dans categorie
#pour l'instant on ne peut pas passer de theme et qu'une couleur
#vérifier si la couleur existe déja et les contraindre à 3 couleurs maxi
#couleur joker
def addClothe(request):
    data = {}
    success = False
    themes = []
    currentUser = request.user

    if currentUser.is_authenticated():
        if request.method == "POST":
            form = AddClotheForm(request.POST, user=request.user)
            if form.is_valid():
                warmthC = form.cleaned_data["warmth"]
                photoC = form.cleaned_data["photo"]
                categoryC = Category.objects.get(name = form.cleaned_data["category"], area = form.cleaned_data["area"])
                themesC = form.cleaned_data["themes"]
                colorsC = form.cleaned_data["color"]

                newClothe = Clothe(warmth = warmthC, photo = photoC, state = 0, nbreUse = 0, category = categoryC, user = currentUser)
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
                    success = True
                else:
                    data['message'] = 'Error during creation of clothe'
                        
                

            else: # si form non valide
                data['message'] = 'Form not validated'
                
            
            #return HttpResponse(json.dumps(data), content_type='application/json')

        else: #si non post

            ####################
            if currentUser.is_authenticated():
                form = AddClotheForm(user=request.user)
                '''themesFromUser = Theme.objects.filter(userOwner = currentUser)
                for theme in themesFromUser:
                    themes.append(theme.name)
                data = {'themes':themes}'''
            else:
                return HttpResponseForbidden('User is not authenticated')
            ####################
            
            data['message'] = 'Need a POST request'
            data['success'] = success
            
    else:
        return HttpResponseForbidden('User is not authenticated')

    data['success'] = success
    #return render(request, 'dressingManage/addClothe.html', locals())
    return HttpResponse(json.dumps(data), content_type='application/json')


def getAllClothes(request):
    data = {}
    success = False
    clothes = []
    photos = []
    currentUser = request.user
    if currentUser.is_authenticated():
        clothesFromUser = Clothe.objects.filter(user = currentUser)
        for clothe in clothesFromUser:
            photos.append(clothe.pk)
        data['clothes'] = photos
        success = True
    else:
        return HttpResponseForbidden('User is not authenticated')

    data['success'] = success
    return HttpResponse(json.dumps(data), content_type='application/json')

#faire un form pour passer string
def createTheme(request):
    '''data = {}
    li1 = []
    li2 = []
    li1.append('wesh')
    li1.append('yolo')

    data['phrase']=li1
    #data = {'Phrase_swag':li1}

    li2.append('Yo')
    li2.append('Maggle')

    data['Jean']=li2'''
    

    return HttpResponse(json.dumps(data), content_type='application/json')

def getThemes(request):
    data = {}
    success = False
    themes = []
    currentUser = request.user
    
    if currentUser.is_authenticated():
        themesFromUser = Theme.objects.filter(userOwner = currentUser)
        for theme in themesFromUser:
            themes.append(theme.name)
        data['themes'] = themes
        success = True
    else:
        return HttpResponseForbidden('User is not authenticated')
        
    data['success'] = success
    
    #return render(request, 'dressingManage/addClothe.html', locals())
    return HttpResponse(json.dumps(data), content_type='application/json')
