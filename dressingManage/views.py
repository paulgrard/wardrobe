# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, Http404
from dressingManage.forms import AddClotheForm, AddThemeForm, GetThemeForm, forms
from django.contrib.auth.models import User
from dressingManage.models import Clothe, Category, Color, Theme
import json


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
            form = AddClotheForm(request.POST) #old arguments , user=request.user
            if form.is_valid():
                warmthC = form.cleaned_data["warmth"]
                photoC = form.cleaned_data["photo"]
                categoryC = Category.objects.get(name = form.cleaned_data["category"], area = form.cleaned_data["area"])
                themesC = form.cleaned_data["themes"]
                color1C = form.cleaned_data["color1"]
                color2C = form.cleaned_data["color2"]
                color3C = form.cleaned_data["color3"]
                colorsC = [color1C]

                if color2C:
                    colorsC.append(color2C)

                if color3C:
                    colorsC.append(color3C)

                newClothe = Clothe(warmth = warmthC, photo = photoC, state = 0, nbreUse = 0, category = categoryC, user = currentUser)
                newClothe.save()
                if themesC:
                    #newClothe.themes.add(themesC)
                    for i in themesC.split("-"):
                        try:
                            thm = Theme.objects.get(id = int(i), userOwner=request.user)
                            newClothe.themes.add(thm)
                        except Theme.DoesNotExist:
                            data['success'] = False
                            data['message'] = 'Un des thèmes n\'existe pas.'
                    
                            return HttpResponse(json.dumps(data), content_type='application/json')
                    
                #for valColor in colorsC:
                if len(colorsC)>3:
                    data['success'] = False
                    data['message'] = 'Plus de 3 couleurs passées en paramètres.'
                    
                    return HttpResponse(json.dumps(data), content_type='application/json')

                else:
                    for c in colorsC:
                        try:
                            colorAlrdyExist = Color.objects.get(color = c)
                            newClothe.colors.add(colorAlrdyExist)
                        except Color.DoesNotExist:
                            col = Color(color = c)
                            col.save()
                            newClothe.colors.add(col)
                
                if newClothe:
                    success = True
                else:
                    data['message'] = 'Erreur lors de la création du vêtement.'
                        
                

            else: # si form non valide
                data['message'] = 'Formulaire non valide.'
                
            
            #return HttpResponse(json.dumps(data), content_type='application/json')

        else: #si non post

            ####################
            if currentUser.is_authenticated():
                form = AddClotheForm()#old parameters user=request.user
            else:
                return HttpResponseForbidden('Utilisateur non authentifié')
            ####################
            
            data['message'] = 'Une requête POST est nécessaire.'
            
    else:
        return HttpResponseForbidden('Utilisateur non authentifié')

    data['success'] = success
    return render(request, 'dressingManage/addClothe.html', locals())
    return HttpResponse(json.dumps(data), content_type='application/json')


def getAllClothes(request):
    data = {}
    success = False
    clothes = []
    pKey = {}    
    
    
    currentUser = request.user
    if currentUser.is_authenticated():
        clothesFromUser = Clothe.objects.filter(user = currentUser)
        for clothe in clothesFromUser:
            themes = []
            colors = []
            temp = {}
            categ = get_object_or_404(Category, name = clothe.category.name)

            temp['warmth'] = clothe.warmth
            temp['photo'] = clothe.photo
            temp['state'] = clothe.state
            temp['nbrUse'] = clothe.nbreUse
            temp['category'] = clothe.category.name
            temp['warmthCategory'] = categ.warmth
            temp['area'] = categ.area
            for t in clothe.themes.all():
                themes.append(str(t))
            temp['themes'] = themes
            
            for c in clothe.colors.all():
                colors.append(str(c))
            temp['colors'] = colors
            
            pKey[clothe.pk] = temp
            #pKey.append(clothe.pk)
        data['clothes'] = pKey
        success = True
    else:
        return HttpResponseForbidden('Utilisateur non authentifié')

    data['success'] = success
    return HttpResponse(json.dumps(data), content_type='application/json')



def getClothesFromCategory(request, nameC):
    data = {}
    success = False
    clothes = []
    pKey = []
    currentUser = request.user
    if currentUser.is_authenticated():
        clothesFromCat = Clothe.objects.filter(user = currentUser, category = nameC)
        for clothe in clothesFromCat:
            pKey.append(clothe.pk)
        data['clothes'] = pKey
        success = True
    else:
        return HttpResponseForbidden('Utilisateur non authentifié')

    data['success'] = success
    return HttpResponse(json.dumps(data), content_type='application/json')



#faire un form pour passer string
def addTheme(request):
    data = {}
    success = False
    themes = []
    currentUser = request.user

    if currentUser.is_authenticated():
        if request.method == "POST":
            form = AddThemeForm(request.POST)
            if form.is_valid():
                nameT = form.cleaned_data["name"]

                
                themesFromUser = Theme.objects.filter(userOwner = currentUser)
                for theme in themesFromUser:
                    if theme.name == nameT:
                        data['message'] = 'Ce nom est déja utilisé.'
                        data['success'] = success
                        return HttpResponse(json.dumps(data), content_type='application/json')

                
                newTheme = Theme(name = nameT, userOwner = currentUser)
                newTheme.save()
                    
                '''yolo=newClothe.colors.all()
                for x in yolo:
                    yolo2 = x.color
                data = {'new_clothe':yolo2}
                return HttpResponse(json.dumps(data), content_type='application/json')'''
                    
                if newTheme:
                    success = True
                else:
                    data['message'] = 'Erreur lors de la création du thème.'

            else: # si form non valide
                data['message'] = 'Formulaire non valide.'
                
            
            #return HttpResponse(json.dumps(data), content_type='application/json')

        else: #si non post

            ####################
            if currentUser.is_authenticated():
                form = AddThemeForm()
            else:
                return HttpResponseForbidden('Utilisateur non authentifié')
            ####################
            
            data['message'] = 'Une requête POST est nécessaire.'
            
    else:
        return HttpResponseForbidden('Utilisateur non authentifié')

    data['success'] = success
    return render(request, 'dressingManage/addTheme.html', locals())
    return HttpResponse(json.dumps(data), content_type='application/json')



def getThemes(request):
    data = {}
    success = False
    themes = []
    idTheme = []
    currentUser = request.user
    
    if currentUser.is_authenticated():
        themesFromUser = Theme.objects.filter(userOwner = currentUser)
        for theme in themesFromUser:
            themes.append(theme.name)
            idTheme.append(theme.id)
        
        data['themes'] = themes
        data['id'] = idTheme
        
        success = True
    else:
        return HttpResponseForbidden('Utilisateur non authentifié')
        
    data['success'] = success
    
    #return render(request, 'dressingManage/addClothe.html', locals())
    return HttpResponse(json.dumps(data), content_type='application/json')


def getTheme(request):
    data = {}
    success = False
    currentUser = request.user
    
    if currentUser.is_authenticated():
        if request.method == "POST":
            form = GetThemeForm(request.POST)
            if form.is_valid():
                nameT = form.cleaned_data["name"]
                
                theme = get_object_or_404(Theme, name = nameT, userOwner = currentUser)
                data['theme'] = theme.id
                success = True
                
            else: # si form non valide
                data['message'] = 'Formulaire non valide.'

                
        else: #si non post

            ####################
            if currentUser.is_authenticated():
                form = GetThemeForm()
            else:
                return HttpResponseForbidden('Utilisateur non authentifié')
            ####################
            
            data['message'] = 'Une requête POST est nécessaire.'


            
    else:
        return HttpResponseForbidden('Utilisateur non authentifié')
        
    data['success'] = success
    
    #return render(request, 'dressingManage/getTheme.html', locals())
    return HttpResponse(json.dumps(data), content_type='application/json')
    
def deleteTheme(request, idT):
    data = {}
    success = False
    currentUser = request.user
    
    if currentUser.is_authenticated():
        themeToDel = get_object_or_404(Theme, id = idT, userOwner = currentUser)

        themeToDel.delete()
        success = True
        data['success'] = success
        
    else:
        return HttpResponseForbidden('Utilisateur non authentifié')
    
    return HttpResponse(json.dumps(data), content_type='application/json')


def getColors(request, idC):
    data = {}
    success = False
    currentUser = request.user
    colors = []
    
    if currentUser.is_authenticated():
        clothing = get_object_or_404(Clothe, id = idC, user = currentUser)
        if clothing:
            colorsFromClothe = clothing.colors
            for c in colorsFromClothe.all():
                colors.append(c.color)
            
            data['colors'] = colors
            success = True
        
        else:
            data['message'] = "Vêtement non trouvé."
            
        data['success'] = success
        
    else:
        return HttpResponseForbidden('Utilisateur non authentifié')
    
    return HttpResponse(json.dumps(data), content_type='application/json')



def getAllColors(request):
    data = {}
    success = False
    currentUser = request.user
    colors = []
    
    if currentUser.is_authenticated():
        col = Color.objects.all()
        if col:
            for c in col.all():
                colors.append(c.color)
            
            data['colors'] = colors
            success = True
        
        else:
            data['message'] = "Erreur lors de la requête."
            
        data['success'] = success
        
    else:
        return HttpResponseForbidden('Utilisateur non authentifié')
    
    return HttpResponse(json.dumps(data), content_type='application/json')


from wardrobe.settings import IMG_FOLDER

def getPicture(request, idC):
    data = {}
    success = False
    currentUser = request.user
    if currentUser.is_authenticated():
        clothing = get_object_or_404(Clothe, id = idC, user = currentUser)
        if clothing:
            pict = clothing.photo
            
            image_data = open(IMG_FOLDER+pict, "rb").read()
            success = True
            return HttpResponse(image_data, content_type="image/jpeg")
        else:
            data['message'] = "Erreur lors de la création du vêtement."
        
    else:
        return HttpResponseForbidden('Utilisateur non authentifié')

    data['success'] = success
    return HttpResponse(json.dumps(data), content_type='application/json')
