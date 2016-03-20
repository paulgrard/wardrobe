# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, Http404
from dressingManage.forms import AddClotheForm, AddThemeForm, GetThemeForm, forms, WeatherForm, EditClotheForm, OutfitGenerationForm
from django.contrib.auth.models import User
from dressingManage.models import Clothe, Category, Color, Theme, Quantity, Pattern, Outfit
from userManage.models import Parameters
import json, os
from urllib.request import urlopen
from django.core.files.uploadedfile import TemporaryUploadedFile
from wardrobe.settings import IMG_FOLDER
from django.db.models import Q
import random

def accueil(request):
    return render(request, 'dressingManage/accueil.html')

#penser à renommer les photos et faire une requete avant d'ajouter la photo pour savoir si elle est unique ou non

#couleur joker
def addClothe(request):
    data = {}
    success = False
    themes = []
    currentUser = request.user

    if currentUser.is_authenticated():
        if request.method == "POST":
            form = AddClotheForm(request.POST, request.FILES) #old arguments , user=request.user
            if form.is_valid():
                warmthC = form.cleaned_data["warmth"]
                #photoC = form.cleaned_data["photoOld"]
                categoryC = Category.objects.get(pk = form.cleaned_data["category"], area = form.cleaned_data["area"]) #old    name = form.cleaned_data["category"]
                themesC = form.cleaned_data["themes"]
                color1C = form.cleaned_data["color1"]
                color2C = form.cleaned_data["color2"]
                color3C = form.cleaned_data["color3"]
                colorsC = [color1C]
                quantity1C = form.cleaned_data["quantity1"]
                quantity2C = form.cleaned_data["quantity2"]
                quantity3C = form.cleaned_data["quantity3"]
                quantitiesC = [quantity1C]



                newClothe = Clothe(warmth = warmthC, state = 0, nbreUse = 0, category = categoryC, user = currentUser)
                newClothe.save()

                photoName = str(newClothe.pk) + '.jpg'

                with open(IMG_FOLDER + photoName , 'wb+') as destination:
                    for chunk in request.FILES['photo'].chunks():
                        destination.write(chunk)

                newClothe.photo = photoName
                newClothe.save()

                if color2C and quantity2C:
                    if not quantity2C == 0:
                        colorsC.append(color2C)
                        quantitiesC.append(quantity2C)

                if color3C and quantity3C:
                    if not quantity3C == 0:
                        colorsC.append(color3C)
                        quantitiesC.append(quantity3C)

                if themesC:
                    #newClothe.themes.add(themesC)
                    for i in themesC.split("-"):
                        try:
                            thm = Theme.objects.get(Q(id = int(i)) & (Q(userOwner=request.user) | Q(userOwner=None)))
                            newClothe.themes.add(thm)
                        except Theme.DoesNotExist:
                            data['success'] = False
                            data['message'] = 'Un des thèmes n\'existe pas.'
                            newClothe.themes.remove()
                            newClothe.delete()
                            os.remove(IMG_FOLDER + photoName)
                            return HttpResponse(json.dumps(data), content_type='application/json')

                #for valColor in colorsC:
                if len(colorsC)>3 or len(quantitiesC)>3:
                    data['success'] = False
                    newClothe.delete()
                    os.remove(IMG_FOLDER + photoName)
                    data['message'] = 'Plus de 3 couleurs ou 3 quantitées passées en paramètres.'

                    return HttpResponse(json.dumps(data), content_type='application/json')

                else:
                    for c in colorsC:
                        try:
                            colorAlrdyExist = Color.objects.get(code = c)
                            indice = colorsC.index(c)
                            newQuantity = Quantity(quantity = quantitiesC[indice], color = colorAlrdyExist)
                            newQuantity.save()

                            newClothe.colors.add(colorAlrdyExist)
                            newClothe.quantities.add(newQuantity)

                        except Color.DoesNotExist:
                            '''col = Color(color = c)
                            col.save()
                            newClothe.colors.add(col)'''
                            data['success'] = False
                            data['message'] = 'Une des couleurs n\'existe pas.'
                            newClothe.colors.remove()
                            newClothe.delete()
                            os.remove(IMG_FOLDER + photoName)
                            return HttpResponse(json.dumps(data), content_type='application/json')

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
    #return render(request, 'dressingManage/addClothe.html', locals())
    return HttpResponse(json.dumps(data), content_type='application/json')


def editClothe(request,idC):
    data = {}
    success = True
    themes = []
    colorAlrdyExist = []
    quantitiesToPut = []
    currentUser = request.user

    if currentUser.is_authenticated():
        if request.method == "POST":
            form = EditClotheForm(request.POST, request.FILES) #old arguments , user=request.user
            if form.is_valid():
                warmthC = form.cleaned_data["warmth"]
                #photoC = form.cleaned_data["photo"]
                categoryC = form.cleaned_data["category"] #Category.objects.get(name = form.cleaned_data["category"], area = form.cleaned_data["area"])
                areaC = form.cleaned_data["area"]
                themesC = form.cleaned_data["themes"]
                color1C = form.cleaned_data["color1"]
                color2C = form.cleaned_data["color2"]
                color3C = form.cleaned_data["color3"]
                colorsC = []
                quantity1C = form.cleaned_data["quantity1"]
                quantity2C = form.cleaned_data["quantity2"]
                quantity3C = form.cleaned_data["quantity3"]
                quantitiesC = []


                cloth = get_object_or_404(Clothe, id = int(idC), user=currentUser)

                if categoryC and areaC:
                    cat = get_object_or_404(Category, pk = categoryC, area = areaC)
                    cloth.category = cat

                if not(categoryC) and areaC:
                    success = False
                    data['message'] = 'Le type de vêtement n\'a pas été indiqué.'

                if not(areaC) and categoryC:
                    catArea = cloth.category.area
                    cat = get_object_or_404(Category, pk = categoryC, area = catArea)
                    cloth.category = cat

                if warmthC:
                    cloth.warmth = warmthC


                if form.cleaned_data['photo']:
                    photoName = str(cloth.pk) + '.jpg'
                    os.remove(IMG_FOLDER + photoName)

                    with open(IMG_FOLDER + photoName , 'wb+') as destination:
                        for chunk in request.FILES['photo'].chunks():
                            destination.write(chunk)


                if themesC:
                    for i in themesC.split("-"):
                        try:
                            themes.append(Theme.objects.get(Q(id = int(i)) & (Q(userOwner=request.user) | Q(userOwner=None))))
                        except Theme.DoesNotExist:
                            data['success'] = False
                            data['message'] = 'Un des thèmes n\'existe pas.'

                            return HttpResponse(json.dumps(data), content_type='application/json')
                    cloth.themes.set(themes)


                if color1C:
                    colorsC.append(color1C)
                    quantitiesC.append(quantity1C)
                    colorsC.append(color2C)
                    quantitiesC.append(quantity2C)
                    colorsC.append(color3C)
                    quantitiesC.append(quantity3C)

                    #récupère les anciennes quantités et les supprime de la BDD
                    oldQuant = cloth.quantities
                    for q in oldQuant.all():
                        q.delete()


                    #création des nouvelles couleurs et quantités
                    for c in colorsC:
                        try:
                            colorAlrdyExist.append(Color.objects.get(code = c))

                            indice = colorsC.index(c)
                            newQuantity = Quantity(quantity = quantitiesC[indice], color = Color.objects.get(code = c))
                            newQuantity.save()

                            quantitiesToPut.append(newQuantity)

                        except Color.DoesNotExist:
                            data['success'] = False
                            data['message'] = 'Une des couleurs n\'existe pas.'
                    cloth.colors.set(colorAlrdyExist)
                    cloth.quantities.set(quantitiesToPut)

                cloth.save()


            else: # si form non valide
                data['message'] = 'Formulaire non valide.'


            #return HttpResponse(json.dumps(data), content_type='application/json')

        else: #si non post

            ####################
            if currentUser.is_authenticated():
                form = EditClotheForm()#old parameters user=request.user
            else:
                return HttpResponseForbidden('Utilisateur non authentifié')
            ####################
            success = False
            data['message'] = 'Une requête POST est nécessaire.'

    else:
        return HttpResponseForbidden('Utilisateur non authentifié')

    data['success'] = success
    #return render(request, 'dressingManage/editClothe.html', locals())
    return HttpResponse(json.dumps(data), content_type='application/json')


def getAllClothes(request):
    data = {}
    success = False
    clothes = []
    pKey = []


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
            temp['category'] = clothe.category.pk
            temp['warmthCategory'] = categ.warmth
            temp['area'] = categ.area
            for t in clothe.themes.all():
                themes.append(str(t))
            temp['themes'] = themes

            for c in clothe.colors.all():
                info_colors = {}
                for q in clothe.quantities.all():

                    if q.color == c:
                        info_colors['code'] = str(c.code)
                        info_colors['quantity'] = q.quantity
                colors.append(info_colors)

            temp['colors'] = colors
            temp['id'] = clothe.pk





            pKey.append(temp)
            #pKey.append(clothe.pk)
        data['clothes'] = pKey
        success = True
    else:
        return HttpResponseForbidden('Utilisateur non authentifié')

    data['success'] = success
    return HttpResponse(json.dumps(data), content_type='application/json')




def getClothe(request, idC):
    data = {}
    infos = {}
    success = False
    currentUser = request.user
    clothInfo = []
    colors = []

    if currentUser.is_authenticated():
        cloth = get_object_or_404(Clothe, id = int(idC))
        
        infos['id'] = int(idC)
        infos['warmth'] = cloth.warmth
        infos['photo'] = cloth.photo
        infos['state'] = cloth.state
        infos['category'] = cloth.category.name
        infos['categoryId'] = cloth.category.id
        infos['area'] = cloth.category.area

        infos['themes'] = [{"id":t.id, "name":t.name} for t in cloth.themes.all()]

        for c in cloth.colors.all():
            infos_color = {}
            for q in cloth.quantities.all():
                
                if q.color == c:
                    infos_color['code'] = str(c.code)
                    infos_color['id'] = c.id
                    infos_color['name'] = c.name
                    infos_color['quantity'] = q.quantity
                    colors.append(infos_color)
            
        infos['colors'] = colors
        data['infos'] = infos
        success = True
    else:
        return HttpResponseForbidden('Utilisateur non authentifié')

    data['success'] = success
    return HttpResponse(json.dumps(data), content_type='application/json')





def getClothesFromCategory(request, idC):
    data = {}
    success = False
    clothes = []
    pKey = []
    currentUser = request.user
    if currentUser.is_authenticated():
        categ = get_object_or_404(Category, pk = int(idC))
        clothesFromCat = Clothe.objects.filter(user = currentUser, category = categ)
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
    #return render(request, 'dressingManage/addTheme.html', locals())
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

        themesFromNullUser = Theme.objects.filter(userOwner = None)
        for themeNull in themesFromNullUser:
            themes.append(themeNull.name)
            idTheme.append(themeNull.id)

        data['themes'] = themes
        data['id'] = idTheme

        success = True
    else:
        return HttpResponseForbidden('Utilisateur non authentifié')

    data['success'] = success

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
    temp = {}

    if currentUser.is_authenticated():
        clothing = get_object_or_404(Clothe, id = int(idC), user = currentUser)
        if clothing:
            colorsFromClothe = clothing.colors
            quantFromClothe = clothing.quantities

            for c in colorsFromClothe.all():
                quanti = []
                temp['code'] = c.code
                for q in quantFromClothe.all():
                    quant = Quantity.objects.get(id = q.id, color = c)
                    quanti.append(quant.quantity)

                temp['quantity'] = quanti

                colors.append(temp)
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
                colors.append(c.code)

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
        clothing = get_object_or_404(Clothe, id = int(idC), user = currentUser)
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


def getWeather(request):
    data = {}
    success = False
    currentUser = request.user
    if currentUser.is_authenticated():
        if request.method == "POST":
            form = WeatherForm(request.POST)
            if form.is_valid():
                lon = form.cleaned_data["lon"]
                lat = form.cleaned_data["lat"]
                content = urlopen('http://api.openweathermap.org/data/2.5/find?lat=' + str(lat) + '&lon=' + str(lon) + '&cnt=1&appid=f7dea76625663a7ce872ba2c9c206fec').read().decode("utf-8")
                content = json.loads(content)
                temp = content["list"][0]["main"]["temp"]
                data["temp"] = int(round(temp - 273.15))
                weather = content["list"][0]["weather"][0]["main"]
                data["weather"] = weather
                success = True
            else: # si form non valide
                data['message'] = 'Formulaire non valide.'

        else: #si non post

            ####################
            if currentUser.is_authenticated():
                form = WeatherForm()
                return render(request, 'dressingManage/getWeather.html', locals())
            else:
                return HttpResponseForbidden('Utilisateur non authentifié')
            ####################

            data['message'] = 'Une requête POST est nécessaire.'


    else:
        return HttpResponseForbidden('Utilisateur non authentifié')

    data['success'] = success
    return HttpResponse(json.dumps(data), content_type='application/json')



def getCategoriesFromArea(request,idA):
    data = {}
    name = []
    idC = []
    temp = []
    success = False
    currentUser = request.user
    if currentUser.is_authenticated():

        cats = Category.objects.filter(area = int(idA))
        for c in cats:
            cat = {}
            cat["name"] = c.name
            cat["id"] = c.pk
            temp.append(cat)
        data["categories"] = temp
        success = True

    else:
        return HttpResponseForbidden('Utilisateur non authentifié')

    data['success'] = success
    return HttpResponse(json.dumps(data), content_type='application/json')


def changeState(request, idC, state):
    data = {}
    success = False
    currentUser = request.user

    if currentUser.is_authenticated():
        cloth = Clothe.objects.get(id = int(idC), user=currentUser)
        cloth.state = int(state)
        cloth.save()
        success = True

    else:
        return HttpResponseForbidden('Utilisateur non authentifié')

    data['success'] = success
    return HttpResponse(json.dumps(data), content_type='application/json')



def setGenerating(request, generatingState):
    data = {}
    success = False
    currentUser = request.user

    if currentUser.is_authenticated():
        outfit = get_object_or_404(Outfit, userOwner = currentUser)
        if int(generatingState) == 1:
            outfit.generating = True
            outfit.save()
            success = True
        elif int(generatingState) == 0:
            outfit.generating = False
            outfit.save()
            success = True
        else:
            data['success'] = success
            data['message'] = 'La valeur passée en paramètre n\'est pas bonne.'
            
    else:
        return HttpResponseForbidden('Utilisateur non authentifié')

    data['success'] = success
    return HttpResponse(json.dumps(data), content_type='application/json')



def getOutfitSettings(request):
    data = {}
    info = {}
    various = []
    
    success = False
    currentUser = request.user


    if currentUser.is_authenticated():
        outfit = get_object_or_404(Outfit, userOwner = currentUser)

        if outfit.firstLayer:
            temp = {}
            temp['id'] = outfit.firstLayer.id
            temp['photo'] = outfit.firstLayer.photo
            info['firstLayer'] = temp
        else:
            info['firstLayer'] = -1


        if outfit.secondLayer:
            temp = {}
            temp['id'] = outfit.secondLayer.id
            temp['photo'] = outfit.secondLayer.photo
            info['secondLayer'] = temp
        else:
            info['secondLayer'] = -1

        
        if outfit.pant:
            temp = {}
            temp['id'] = outfit.pant.id
            temp['photo'] = outfit.pant.photo
            info['pant'] = temp
        else:
            info['pant'] = -1

        
        if outfit.shoes:
            temp = {}
            temp['id'] = outfit.shoes.id
            temp['photo'] = outfit.shoes.photo
            info['shoes'] = temp
        else:
            info['shoes'] = -1

        
        if outfit.coat:
            temp = {}
            temp['id'] = outfit.coat.id
            temp['photo'] = outfit.coat.photo
            info['coat'] = temp
        else:
            info['coat'] = -1

        
        if outfit.underwear:
            temp = {}
            temp['id'] = outfit.underwear.id
            temp['photo'] = outfit.underwear.photo
            info['underwear'] = temp
        else:
            info['underwear'] = -1

        
        if outfit.underwearTop:
            temp = {}
            temp['id'] = outfit.underwearTop.id
            temp['photo'] = outfit.underwearTop.photo
            info['underwearTop'] = temp
        else:
            info['underwearTop'] = -1

        
        if outfit.sock:
            temp = {}
            temp['id'] = outfit.sock.id
            temp['photo'] = outfit.sock.photo
            info['sock'] = temp
        else:
            info['sock'] = -1
            
        for c in outfit.various.all():
            variousTemp = {}
            cloth = Clothe.objects.get(id = c.id, user = currentUser)
            variousTemp['id'] = c.id
            variousTemp['photo'] = c.photo
            various.append(variousTemp)
            
        info['various'] = various
        info['generating'] = outfit.generating
        info['nbrLayer'] = outfit.nbrLayer
        info['theme'] = outfit.theme.id

        data['settings'] = info
        success = True
    else:
        return HttpResponseForbidden('Utilisateur non authentifié')

    data['success'] = success
    return HttpResponse(json.dumps(data), content_type='application/json')   




    

from collections import Counter


def generateOutfit(request):
    data = {}
    success = False
    currentUser = request.user
    lCoulIds = []
    lCoulPant = []
    lCoulIdsUnderwear = []
    lSecondLayerIds = []
    lFirstLayerIds = []
    lPantIds = []
    lCoatIds = []
    lShoesIds = []
    lHeadgeardIds = []
    lCapIds = []
    tempo = {}
    cloth = {}
    various = []

    SecondLayer = FirstLayer = pant = coat = shoes = underwear = underwearTop = sock = cap = headgear = scarf = glove = bonnet = hood = foulard = cravat = bag= -1

    
    if currentUser.is_authenticated():
        if request.method == "POST":
            form = OutfitGenerationForm(request.POST)
            if form.is_valid():
                '''try:
                    outfit = Outfit.objects.get(userOwner = currentUser)
                except Outfit.DoesNotExist:
                    outfit = Outfit(userOwner = currentUser)
                    outfit.save()'''
                
                
                
                outfit, created = Outfit.objects.get_or_create(userOwner = currentUser)
                
                outfit.generating = True

                
                    
                lon = form.cleaned_data["lon"]
                lat = form.cleaned_data["lat"]
                themesC = form.cleaned_data["themes"]

                # récupère weather
                #content = urlopen('http://api.openweathermap.org/data/2.5/find?lat=' + str(lat) + '&lon=' + str(lon) + '&cnt=1&appid=f7dea76625663a7ce872ba2c9c206fec').read().decode("utf-8")
                content = urlopen('http://api.openweathermap.org/data/2.5/forecast/daily?lat=' + str(lat) + '&lon=' + str(lon) + '&cnt=1&appid=f7dea76625663a7ce872ba2c9c206fec').read().decode("utf-8")
                #content = urlopen('http://api.openweathermap.org/data/2.5/forecast/daily?lat=' + str(lat) + '&lon=' + str(lon) + 'cnt=5&appid=f7dea76625663a7ce872ba2c9c206fec').read().decode("utf-8")
                #http://api.openweathermap.org/data/2.5/forecast?lat=35&lon=139&appid=b1b15e88fa797225412429c1c50c122a
                content = json.loads(content)
                #data['con']=content
                '''i = 1
                temp = 0
                while i!=5:
                    temp += content["list"][i]["temp"]
                    i++
                '''
                #temp = content["list"][0]["main"]["temp"]
                tempD = content["list"][0]["temp"]["day"]
                #data["tempD"] = tempD 
                tempE = content["list"][0]["temp"]["eve"]
                #data["tempE"] = tempE 
                tempM = content["list"][0]["temp"]["morn"]
                #data["tempM"] =tempM 
                temp = ( tempD + tempE + tempM )/3
                temp = int(round(temp - 273.15))
                data["temp"] = temp
                weather = content["list"][0]["weather"][0]["main"]
                weatherDescription = content["list"][0]["weather"][0]["description"]
                #"light rain"
                data["weather"] = weather

                # récupère thèmes
                if themesC:
                    try:
                        thm = Theme.objects.get(Q(id = themesC) & (Q(userOwner=request.user) | Q(userOwner=None)))
                    except Theme.DoesNotExist:
                        data['success'] = False
                        data['message'] = 'Un des thèmes n\'existe pas.'

                        return HttpResponse(json.dumps(data), content_type='application/json')
                    

                # détermine nbre couches
                if temp >= 21:
                    outfitLayers = 1
                else:
                    outfitLayers = 2


                outfit.nbrLayer = outfitLayers
                outfit.theme = thm
                outfit.save()

                

                ptsTop = 0
                ptsPant = 0
                ptsCoat = 0
                ptsShoes = 0
                ptsVarious = 0
                    

                if temp > 30:
                    ptsTop = 2
                    ptsPant = 2
                    ptsCoat = 0
                    ptsShoes = 2
                    ptsVarious = 2
                    
                if temp in range(25, 30): 
                    ptsTop = 3
                    ptsPant = 3
                    ptsCoat = 0
                    ptsShoes = 3
                    ptsVarious = 3
                    
                if temp in range(20, 25):
                    ptsTop = 4
                    ptsPant = 4
                    ptsCoat = 4
                    ptsShoes = 4
                    ptsVarious = 4
                    
                if temp in range(15, 20):
                    ptsTop = 8
                    ptsPant = 6
                    ptsCoat = 7
                    ptsShoes = 5
                    ptsVarious = 5
                    
                if temp in range(10, 15):
                    ptsTop = 14
                    ptsPant = 7
                    ptsCoat = 10
                    ptsShoes = 7
                    ptsVarious = 9
                    
                if temp in range(5, 10):
                    ptsTop = 16
                    ptsPant = 8
                    ptsCoat = 14
                    ptsShoes = 10
                    ptsVarious = 18
                    
                if  temp in range(0, 5):
                    ptsTop = 18
                    ptsPant = 9
                    ptsCoat = 17
                    ptsShoes = 12
                    ptsVarious = 26
                    
                if temp in range(-5, 0):
                    ptsTop = 20
                    ptsPant = 9
                    ptsCoat = 18
                    ptsShoes = 13
                    ptsVarious = 31
                    
                if  temp in range(-10, -5):
                    ptsTop = 22
                    ptsPant = 9
                    ptsCoat = 19
                    ptsShoes = 14
                    ptsVarious = 33
                    
                if temp <= -10:
                    ptsTop = 24
                    ptsPant = 9
                    ptsCoat = 20
                    ptsShoes = 15
                    ptsVarious = 35
                    


                
                #############################################
                    
                
                # choisir le vêtement de la seconde couche
                if outfitLayers == 2:

                    ptsFirst = int(ptsTop/3)
                    ptsSecond = ptsTop - ptsFirst
                                                            #appartient au user     est dans le theme                           appartient à la couche 2 ou 0
                    lSecondLayer = Clothe.objects.filter(Q(user = currentUser) & Q(themes = thm) & Q(category__area = 1) & (Q(category__layer = 2) | Q(category__layer = 0)))
                    
                    if lSecondLayer:
                        for c in lSecondLayer:
                            #cat = Category.objects.get(id = c.category.id) # on récupère la catégorie et on calcule les points totaux des warmth de la cat et du vêt
                            warmthTot = c.category.warmth * c.warmth
                            if (warmthTot >= (ptsSecond-1)) and (warmthTot <= (ptsSecond+1)): #si les points totaux sont +-1 de ptsSecond, on ajout le vêt à la liste
                                lSecondLayerIds.append(c.id)  # crée la liste d'ids de vêtements possibles
                        
                        
                        if len(lSecondLayerIds) == 0:
                            SecondLayer = -1
                            cloth['secondLayer'] = SecondLayer
                        else:
                            SecondLayer = Clothe.objects.get(id = random.choice(lSecondLayerIds))
                            cloth['id'] = SecondLayer.id
                            cloth['photo']= SecondLayer.photo
                            #SecondLayerId = SecondLayer.id
                            

                            # crée la liste des couleurs
                            lCoul = SecondLayer.colors
                            for c in lCoul.all():
                                quant = Quantity.objects.get(id = SecondLayer.quantities.all(), color = c)
                                '''for q in SecondLayer.quantities.all():
                                    quant = Quantity.objects.get(id = q.id, color = c)'''
                                
                                if quant.quantity >= 20:   
                                    if c.id == 1 or c.id == 2: # si noir ou blanc 
                                        if len(lCoulIds) == 0: # et si liste vide on ajoute tout
                                            lCoulIds = list(range(1, 25))
                                            
                                        '''else: # et si liste déja remplie on ajoute tout et on garde seulement les doublons           !!!!!!!!!!!!! ne sert à rien !!!
                                            lCoulIds = lCoulIds + list(range(1, 25))
                                            counts = Counter(lCoulIds)
                                            lCoulIds = [value for value, count in counts.items() if count > 1]'''
                                    else: #si pas noir ni blc
                                        pat = Pattern.objects.get(id = c.id) # on récupère le pattern correspondant
                                        if len(lCoulIds) == 0: # si liste vide on ajoute les couleurs
                                            for col in pat.colors.all():
                                                lCoulIds.append(col.id)
                                        else: # sinon on ajoute les couleurs et on garde seulement les doublons
                                            for col in pat.colors.all():
                                                lCoulIds.append(col.id)
                                            counts = Counter(lCoulIds)
                                            lCoulIds = [value for value, count in counts.items() if count > 1]
                            
                            lCoulIds.append(1) # on ajoute le blanc et le noir qui sont compatible avec tout
                            lCoulIds.append(2)
                            lCoulIds = list(set(lCoulIds))
                            #data['lCoulIds'] = list(lCoulIds)
                            
                            
                               
                    else:
                        SecondLayer = -1
                        cloth['secondLayer'] = SecondLayer

                    tempo['secondLayer']=cloth
                    




                    
                    # génération du pantalon
                    cloth = {}
                    if SecondLayer == -1:
                        lCoulIds = list(range(1, 25))
                                                                                                                                            #jeans id = 31                    
                    lPant = Clothe.objects.filter(Q(user = currentUser) & Q(themes = thm) & Q(category__area = 2) & (Q(colors__id__in = lCoulIds) | Q(category__id = 31)))

                    if lPant:
                        for c in lPant:
                            warmthTot = c.category.warmth * c.warmth
                            if (warmthTot >= (ptsPant-1)) and (warmthTot <= (ptsPant+1)):
                                lPantIds.append(c.id)

                        if len(lPantIds) == 0:
                            pant = -1
                            cloth['id'] = pant
                        else:
                            pant = Clothe.objects.get(id = random.choice(lPantIds))

                            lCoulPant = pant.colors

                            for c in lCoulPant.all():
                                quant = Quantity.objects.get(id = pant.quantities.all(), color = c)
                                if quant.quantity >= 20:
                                    lCoulIds.append(1) 
                                    lCoulIds.append(2)

                                    lCoulIds = list(set(lCoulIds))
                                    
                                    if c.id!= 1 and c.id!=2: #si pas blc ni noir
                                        pat = Pattern.objects.get(id = c.id) # on récupère le pattern correspondant
                                        for col in pat.colors.all(): # on ajoute les couleurs
                                            lCoulIds.append(col.id)
                                        counts = Counter(lCoulIds) #et on garde que les doublons
                                        lCoulIds = [value for value, count in counts.items() if count > 1]

                            #data['lCoulIds'] = lCoulIds
                            cloth['id'] = pant.id
                            cloth['photo']= pant.photo
                            lCoulIds.append(1) 
                            lCoulIds.append(2)

                            lCoulIds = list(set(lCoulIds))
                            #data['lCoulIds'] = list(lCoulIds)
                    else:
                        pant = -1
                        cloth['id'] = pant
                        
                    tempo['pant'] = cloth

                        
                    

                    # choisir le vêtement de la 1ere couche (si 2eme couche)
                    cloth = {}
                    
                    lFirstLayer = Clothe.objects.filter(Q(user = currentUser) & Q(themes = thm) & Q(category__area = 1) & Q(colors__id__in = lCoulIds) & (Q(category__layer = 1) | Q(category__layer = 0)))
                    # pour être sur de ne pas avoir le même que celui de la 2eme couche il faudrait Q(id != SecondLayer.id) mais s'il y est, erreur de type : 'bool' object is not iterable
                    
                        
                    if lFirstLayer:
                        for c in lFirstLayer:
                            #cat = Category.objects.get(id = c.category.id) # on récupère la catégorie et on calcule les points totaux des warmth de la cat et du vêt
                            warmthTot = c.category.warmth * c.warmth
                            if (warmthTot >= (ptsFirst-1)) and (warmthTot <= (ptsFirst+1)):
                                lFirstLayerIds.append(c.id)


                        if len(lFirstLayerIds) == 0:
                            FirstLayer = -1
                            cloth['id'] = FirstLayer
                        else:
                            FirstLayer = Clothe.objects.get(id = random.choice(lFirstLayerIds))

                            lCoul = FirstLayer.colors

                            for c in lCoul.all():
                                quant = Quantity.objects.get(id = FirstLayer.quantities.all(), color = c)
                                if quant.quantity >= 20:
                                    
                                    lCoulIds.append(1) 
                                    
                                    lCoulIds.append(2)
                                    
                                    lCoulIdsF = set(lCoulIds)
                                   
                                    lCoulIdsF = list(lCoulIdsF)
                                    #data['lCoulIdsF'] = lCoulIdsF
                                    if c.id!= 1 and c.id!=2: #si pas blc ni noir
                                        pat = Pattern.objects.get(id = c.id) # on récupère le pattern correspondant
                                        for col in pat.colors.all(): # on ajoute les couleurs
                                            lCoulIds.append(col.id)
                                        counts = Counter(lCoulIds) #et on garde que les doublons
                                        lCoulIds = [value for value, count in counts.items() if count > 1]


                            cloth['id'] = FirstLayer.id
                            cloth['photo']= FirstLayer.photo

                            lCoulIds.append(1) 
                            lCoulIds.append(2)
                            lCoulIdsF = set(lCoulIds)
                            #data['lCoulIds'] = list(lCoulIds)
                    else:
                        FirstLayer = -1
                        data['id'] = FirstLayer

                    tempo['firstLayer'] = cloth
                    

            ############################################################


                        
                # choisir le vêtement de la 1ere couche (si pas 2eme couche)
                else:
                    cloth = {}
                    lFirstLayer = Clothe.objects.filter(Q(user = currentUser) & Q(themes = thm) & Q(category__area = 1) & (Q(category__layer = 1) | Q(category__layer = 0)))


                    cloth = {}
                    if lFirstLayer:
                        for c in lFirstLayer:
                            #cat = Category.objects.get(id = c.category.id) # on récupère la catégorie et on calcule les points totaux des warmth de la cat et du vêt
                            warmthTot = c.category.warmth * c.warmth
                            if (warmthTot >= (ptsTop-1)) and (warmthTot <= (ptsTop+1)):
                                lFirstLayerIds.append(c.id)  # crée la liste d'ids de vêtements possibles

                        if len(lFirstLayerIds) == 0:
                            FirstLayer = -1
                            cloth['id'] = FirstLayer
                        else:
                            FirstLayer = Clothe.objects.get(id = random.choice(lFirstLayerIds))
                            cloth['id'] = FirstLayer.id
                            cloth['photo'] = FirstLayer.photo

                            # crée la liste des couleurs
                            lCoul = FirstLayer.colors
                            for c in lCoul.all():
                                quant = Quantity.objects.get(id = FirstLayer.quantities.all(), color = c)
                                if quant.quantity >= 20:
                                    if c.id == 1 or c.id == 2: # si noir ou blanc 
                                        if len(lCoulIds) == 0: # et si liste vide on ajoute tout
                                            lCoulIds = list(range(1, 25))
                                        '''else: # et si liste déja remplie on ajoute tout et on garde seulement les doublons
                                            lCoulIds = lCoulIds + list(range(1, 25))
                                            counts = Counter(lCoulIds)
                                            lCoulIds = [value for value, count in counts.items() if count > 1]'''
                                    else: #si pas noir ni blc
                                        pat = Pattern.objects.get(id = c.id) # on récupère le pattern correspondant
                                        if len(lCoulIds) == 0: # si liste vide on ajoute les couleurs
                                            for col in pat.colors.all():
                                                lCoulIds.append(col.id)
                                        else: # sinon on ajoute les couleurs et on garde seulement les doublons
                                            for col in pat.colors.all():
                                                lCoulIds.append(col.id)
                                            counts = Counter(lCoulIds)
                                            lCoulIds = [value for value, count in counts.items() if count > 1]

                            lCoulIds.append(1) # on ajoute le blanc et le noir qui sont compatible avec tout
                            lCoulIds.append(2)
                            lCoulIds = list(set(lCoulIds))
                            #data['lCoulIds'] = list(lCoulIds)   
                    else:
                        FirstLayer = -1
                        cloth['id'] = FirstLayer


                    tempo['firstLayer'] = cloth


                    
                # génération du pantalon
                    cloth = {}
                    lPant = Clothe.objects.filter(Q(user = currentUser) & Q(themes = thm) & Q(category__area = 2) & (Q(colors__id__in = lCoulIds) | Q(category__id = 31)))

                    if lPant:
                        for c in lPant:
                            warmthTot = c.category.warmth * c.warmth
                            if (warmthTot >= (ptsPant-1)) and (warmthTot <= (ptsPant+1)):
                                lPantIds.append(c.id)

                        if len(lPantIds) == 0:
                            pant = -1
                            cloth['id'] = pant
                        else:
                            pant = Clothe.objects.get(id = random.choice(lPantIds))

                            lCoulPant = pant.colors

                            for c in lCoulPant.all():
                                quant = Quantity.objects.get(id = pant.quantities.all(), color = c)
                                if quant.quantity >= 20:
                                    lCoulIds.append(1) 
                                    lCoulIds.append(2)

                                    lCoulIds = list(set(lCoulIds))
                                    
                                    if c.id!= 1 and c.id!=2: #si pas blc ni noir
                                        pat = Pattern.objects.get(id = c.id) # on récupère le pattern correspondant
                                        for col in pat.colors.all(): # on ajoute les couleurs
                                            lCoulIds.append(col.id)
                                        counts = Counter(lCoulIds) #et on garde que les doublons
                                        lCoulIds = [value for value, count in counts.items() if count > 1]

                            
                            cloth['id'] = pant.id
                            cloth['photo'] = pant.photo
                            lCoulIds.append(1) 
                            lCoulIds.append(2)

                            lCoulIds = list(set(lCoulIds))
                            #data['lCoulIds'] = list(lCoulIds)
                    else:
                        pant = -1
                        cloth['id'] = pant
                        
                    tempo['pant'] = cloth


                ################################################
                '''Thunderstorm
                Drizzle
                Rain
                Snow
                Clear
                Clouds
                Extreme'''


                # generation du manteau
                cloth = {}
                if ptsCoat != 0:
                    if pant!=-1:
                        lCoulPId = [c.id for c in lCoulPant.all()]
                        lCoulIdsCoat = [c for c in list(lCoulIds) if c not in lCoulPId]
                        lCoulIdsCoat.append(1)
                        lCoulIdsCoat.append(2)
                        lCoulIdsCoat = list(set(lCoulIdsCoat))
                    else:
                        lCoulIdsCoat = lCoulIds
                    lCoat = Clothe.objects.filter(Q(user = currentUser) & Q(themes = thm) & Q(category__area = 1) & Q(category__layer = 3) & Q(colors__id__in = lCoulIdsCoat))

                    if lCoat:
                        for c in lCoat:
                            warmthTot = c.category.warmth * c.warmth
                            if (warmthTot >= (ptsCoat-3)) and (warmthTot <= (ptsCoat+3)):
                                lCoatIds.append(c.id)

                        if len(lCoatIds) == 0:
                            cloth['id'] = -1
                        else:
                            coat = Clothe.objects.get(id = random.choice(lCoatIds))

                            #data['lCoulIdsCoat'] = list(lCoulIdsCoat)
                            
                            cloth['id'] = coat.id
                            cloth['photo'] = coat.photo
                    else:
                        coat = -1
                        cloth['id'] = coat

                    tempo['coat'] = cloth

                elif weather == "Rain":
                        
                    lCoat = Clothe.objects.filter(Q(user = currentUser) & Q(themes = thm) & Q(category__area = 1) & Q(category__layer = 3) & Q(category__id = 25))
                    

                    if lCoat:
                        coat = Clothe.objects.get(id = random.choice(lCoat.id))
                        cloth['id'] = coat.id
                        cloth['photo'] = coat.photo
                    else:
                        coat = -1
                        cloth['id'] = coat


                    tempo['coat'] = cloth




                ##############################

                # generation des chaussures

                cloth = {}

                if (type(SecondLayer) is not int) and SecondLayer.id == 10: # si veste costume
                    lShoes = Clothe.objects.filter(Q(user = currentUser) & Q(themes = thm) & Q(category__area = 3) & (Q(category__layer = 50) | Q(category__layer = 39) | Q(category__layer = 40)) & Q(colors__id__in = lCoulIds))
                    if lShoes:
                        lShoesIds = [c.id for c in lShoes]
                        shoes = Clothe.objects.get(id = random.choice(lShoesIds))
                        cloth['id'] = shoes.id
                        cloth['photo'] = shoes.photo
                    else:
                        shoes = -1
                        cloth['id'] = -1

                else:
                    lShoes = Clothe.objects.filter(Q(user = currentUser) & Q(themes = thm) & Q(category__area = 3) & Q(colors__id__in = lCoulIds))
                    if lShoes:
                        for c in lShoes:
                            warmthTot = c.category.warmth * c.warmth
                            if (warmthTot >= (ptsShoes-1)) and (warmthTot <= (ptsShoes+1)):
                                lShoesIds.append(c.id)

                        if len(lShoesIds) == 0:
                            cloth['id'] = -1
                        else:
                            shoes = Clothe.objects.get(id = random.choice(lShoesIds))
                            cloth['id'] = shoes.id
                            cloth['photo'] = shoes.photo
                    else:
                        shoes = -1
                        cloth['id'] = shoes

                tempo['shoes'] = cloth


                
                ###################################

                # generation des sous vêtements

                cloth = {}
                
                param = Parameters.objects.get(user = currentUser)
                if param.sex == 2: #si femme
                    lUnderwear = Clothe.objects.filter(Q(user = currentUser) & Q(themes = thm) & Q(category__area = 4) & (Q(category__id = 58) | Q(category__id = 56) | Q(category__id = 55) | Q(category__id = 54) | Q(category__id = 53)))

                    if lUnderwear:
                        lUnderwearIds = [c.id for c in lUnderwear]
                        underwear = Clothe.objects.get(id = random.choice(lUnderwearIds))

                        for c in underwear.color.all():
                            pat = Pattern.objects.get(id = c.id)
                            for col in pat.colors.all():
                                lCoulIdsUnderwear.append(col.id)
                        lCoulIdsUnderwear = list(set(lCoulIdsUnderwear))
                        cloth['id'] = underwear.id
                        cloth['photo'] = underwear.photo

                    else:
                        cloth['id'] = -1

                    tempo['underwear'] = cloth
                    
                    #select top en fonction des couleurs
                    cloth = {}
                    lUnderwearTop = Clothe.objects.filter(Q(user = currentUser) & Q(themes = thm) & Q(category__area = 4) & (Q(category__id = 59) | Q(category__id = 64)) & Q(colors__id__in = lCoulIdsUnderwear))

                    if lUnderwearTop:
                        lUnderwearTopIds = [c.id for c in lUnderwearTop]
                        underwearTop = Clothe.objects.get(id = random.choice(lUnderwearTopIds))
                        cloth['id'] = underwearTop.id
                    else: # si il n'y a rien on essaye sans les couleurs
                        lUnderwearTop = Clothe.objects.filter(Q(user = currentUser) & Q(themes = thm) & Q(category__area = 4) & (Q(category__id = 59) | Q(category__id = 64)))

                        if lUnderwearTop:
                            lUnderwearTopIds = [c.id for c in lUnderwearTop]
                            underwearTop = Clothe.objects.get(id = random.choice(lUnderwearTopIds))
                            cloth['id'] = underwearTop.id
                            cloth['photo'] = underwearTop.photo
                        else:
                            cloth['id'] = -1

                    tempo['underwearTop'] = cloth


                    #generation des chaussettes, bas, collants ....
                    cloth = {}
                    if shoes != -1 and (shoes.categoy.id == 40 or shoes.categoy.id == 42 or shoes.categoy.id == 47):
                        lSock = Clothe.objects.filter(Q(user = currentUser) & Q(themes = thm) & Q(category__area = 4) & (Q(category__id = 62) | Q(category__id = 61)))
                        
                        if lSock:
                            lSockIds = [c.id for c in lSock]
                            sock = Clothe.objects.get(id = random.choice(lSockIds))
                            cloth['id'] = sock.id
                            cloth['photo'] = sock.photo
                        else:
                            cloth['id'] = -1

                        tempo['sock'] = cloth
                        
                    elif shoes != -1 and (shoes.categoy.id == 38 or shoes.categoy.id == 39 or shoes.categoy.id == 45 or shoes.categoy.id == 46 or shoes.categoy.id == 50 or shoes.categoy.id == 51 or shoes.categoy.id == 52):
                        lSock = Clothe.objects.filter(Q(user = currentUser) & Q(themes = thm) & Q(category__area = 4) & (Q(category__id = 63) | Q(category__id = 62) | Q(category__id = 61) | Q(category__id = 60)))
                        
                        if lSock:
                            lSockIds = [c.id for c in lSock]
                            sock = Clothe.objects.get(id = random.choice(lSockIds))
                            cloth['id'] = sock.id
                            cloth['photo'] = sock.photo
                        else:
                            cloth['id'] = -1

                        tempo['sock'] = cloth
                        
                    else:
                        lSock = Clothe.objects.filter(Q(user = currentUser) & Q(themes = thm) & Q(category__area = 4) & (Q(category__id = 63) | Q(category__id = 62) | Q(category__id = 61) | Q(category__id = 60)))
                        
                        if lSock:
                            lSockIds = [c.id for c in lSock]
                            sock = Clothe.objects.get(id = random.choice(lSockIds))
                            cloth['id'] = sock.id
                            cloth['photo'] = sock.photo
                        else:
                            cloth['id'] = -1

                        tempo['sock'] = cloth

                    
                else: #si homme
                    cloth = {}
                    
                    lUnderwear = Clothe.objects.filter(Q(user = currentUser) & Q(themes = thm) & Q(category__area = 4) & (Q(category__id = 58) | Q(category__id = 57) | Q(category__id = 56)))

                    if lUnderwear:
                        lUnderwearIds = [c.id for c in lUnderwear]
                        underwear = Clothe.objects.get(id = random.choice(lUnderwearIds))
                        cloth['id'] = underwear.id
                        cloth['photo'] = underwear.photo

                    else:
                        cloth['id'] = -1

                    tempo['underwear'] = cloth

                    
                    #generation chaussettes
                    cloth = {}
                    if type(shoes) is not int and (shoes.categoy.id == 38 or shoes.categoy.id == 39 or shoes.categoy.id == 45 or shoes.categoy.id == 46 or shoes.categoy.id == 50 or shoes.categoy.id == 51 or shoes.categoy.id == 52):
                        lSock = Clothe.objects.filter(Q(user = currentUser) & Q(themes = thm) & Q(category__area = 4) & (Q(category__id = 63) | Q(category__id = 60)))
                        
                        if lSock:
                            lSockIds = [c.id for c in lSock]
                            sock = Clothe.objects.get(id = random.choice(lSockIds))
                            cloth['id'] = sock.id
                            cloth['photo'] = sock.photo
                        else:
                            cloth['id'] = -1

                        tempo['sock'] = cloth
                        
                    elif shoes == -1:
                        lSock = Clothe.objects.filter(Q(user = currentUser) & Q(themes = thm) & Q(category__area = 4) & (Q(category__id = 63) | Q(category__id = 60)))
                        
                        if lSock:
                            lSockIds = [c.id for c in lSock]
                            sock = Clothe.objects.get(id = random.choice(lSockIds))
                            cloth['id'] = sock.id
                            cloth['photo'] = sock.photo
                        else:
                            cloth['id'] = -1

                        tempo['sock'] = cloth
                        

                ###################################


                #generation des accessoires
                cloth = {}
                # casquette
                if weatherDescription == "Clear" and temp>25:
                    lCap = Clothe.objects.filter(Q(user = currentUser) & Q(themes = thm) & Q(category__area = 5) & Q(category__id = 69))
                    if lCap:
                        lCapIds = [c.id for c in lCap]
                        cap = Clothe.objects.get(id = random.choice(lCapIds))
                        cloth['id'] = cap.id
                        cloth['photo'] = cap.photo

                        various.append(cloth)
                



                # chapeau et beret
                cloth = {}
                if weatherDescription == "Clear" and temp<25 and temp >8:
                    flag = random.randint(0,1)
                    if flag==1:
                        lHeadgear = Clothe.objects.filter(Q(user = currentUser) & Q(themes = thm) & Q(category__area = 5) & (Q(category__id = 68) | Q(category__id = 70)))
                        if lHeadgear:
                            lHeadgeardIds = [c.id for c in lHeadgear]
                            headgear = Clothe.objects.get(id = random.choice(lHeadgearIds))
                            cloth['id'] = headgear.id
                            cloth['photo'] = headgear.photo
                            various.append(cloth)

                # echarpe
                cloth = {}
                if temp<12:
                    lScarf = Clothe.objects.filter(Q(user = currentUser) & Q(themes = thm) & Q(category__area = 5) & Q(category__id = 65))
                    if lScarf:
                        lScarfIds = [c.id for c in lScarf]
                        scarf = Clothe.objects.get(id = random.choice(lScarfIds))
                        cloth['id'] = scarf.id
                        cloth['photo'] = scarf.photo
                        various.append(cloth)
                

                #gants et mitaines
                cloth = {}
                if temp<=8:
                    lGlove = Clothe.objects.filter(Q(user = currentUser) & Q(themes = thm) & Q(category__area = 5) & (Q(category__id = 66) | Q(category__id = 72)))
                    if lGlove:
                        lGloveIds = [c.id for c in lGlove]
                        glove = Clothe.objects.get(id = random.choice(lGloveIds))
                        cloth['id'] = glove.id
                        cloth['photo'] = glove.photo
                        various.append(cloth)

                
                #bonnet
                cloth = {}
                if temp<=8 and temp>-5:
                    lBonnet = Clothe.objects.filter(Q(user = currentUser) & Q(themes = thm) & Q(category__area = 5) & Q(category__id = 67))
                    if lBonnet:
                        lBonnetIds = [c.id for c in lBonnet]
                        bonnet = Clothe.objects.get(id = random.choice(lBonnetIds))
                        cloth['id'] = bonnet.id
                        cloth['photo'] = bonnet.photo
                        various.append(cloth)
                        

                #cagoule
                cloth = {}
                if temp<=-5:
                    lHood = Clothe.objects.filter(Q(user = currentUser) & Q(themes = thm) & Q(category__area = 5) & Q(category__id = 71))
                    if lHood:
                        lHoodIds = [c.id for c in lHood]
                        hood = Clothe.objects.get(id = random.choice(lHoodIds))
                        cloth['id'] = hood.id
                        cloth['photo'] = hood.photo
                        various.append(cloth)


                #etole foulard
                cloth = {}
                if temp>=12 and temp<20:
                    flag = random.randint(0,1)
                    if flag==1:
                        lFoulard = Clothe.objects.filter(Q(user = currentUser) & Q(themes = thm) & Q(category__area = 5) & (Q(category__id = 74) | Q(category__id = 73)))
                        if lFoulard:
                            lFoulardIds = [c.id for c in lFoulard]
                            foulard = Clothe.objects.get(id = random.choice(lFoulardIds))
                            cloth['id'] = foulard.id
                            cloth['photo'] = foulard.photo
                            various.append(cloth)

                

                #noeud pap / cravate
                cloth = {}
                if outfitLayers == 2 and SecondLayer.id == 10:
                    flag = random.randint(0,1)
                    if flag==1:
                        lCravat = Clothe.objects.filter(Q(user = currentUser) & Q(themes = thm) & Q(category__area = 5) & Q(colors__id__in = lCoulIds) & (Q(category__id = 75) | Q(category__id = 76)))
                        if lCravat:
                            lCravatIds = [c.id for c in lCravat]
                            cravat = Clothe.objects.get(id = random.choice(lCravatIds))
                            cloth['id'] = cravat.id
                            cloth['photo'] = cravat.photo
                            various.append(cloth)


                #sac
                cloth = {}
                flag = random.randint(0,1)
                if flag==1:
                    lBag = Clothe.objects.filter(Q(user = currentUser) & Q(themes = thm) & Q(category__area = 5) & Q(colors__id__in = lCoulIds) & (Q(category__id = 77) | Q(category__id = 78) | Q(category__id = 79)))
                    if lBag:
                        lBagIds = [c.id for c in lBag]
                        bag = Clothe.objects.get(id = random.choice(lBagIds))
                        cloth['id'] = bag.id
                        cloth['photo'] = bag.photo
                        various.append(cloth)

                            
                #préparation des data pour le rturn
                if len(various)!=0:
                    tempo['various']=various
                
                data['clothes'] = tempo


                #insertion dans BDD
                
                clothesToPush = []
                
                if SecondLayer != -1:
                    outfit.secondLayer = SecondLayer
                    #outfit.save()
                    #clothesToPush.append(SecondLayer)
                    
                if FirstLayer!=-1:
                    outfit.firstLayer = FirstLayer
                    #outfit.save()
                    #clothesToPush.append(FirstLayer)
                    
                if pant!=-1:
                    outfit.pant = pant
                    #clothesToPush.append(pant)
                    
                if coat!=-1:
                    outfit.coat = coat
                    #clothesToPush.append(coat)
                    
                if shoes!=-1:
                    outfit.shoes = shoes
                    #clothesToPush.append(shoes)
                    
                if underwear!=-1:
                    outfit.underwear = underwear
                    #clothesToPush.append(SecondLayer)
                    
                if underwearTop!=-1:
                    outfit.underwearTop = underwearTop
                    #clothesToPush.append(underwearTop)
                    
                if sock!=-1:
                    outfit.sock = sock
                    #clothesToPush.append(sock)
                    
                if cap!=-1:
                    clothesToPush.append(cap)
                    
                if headgear!=-1:
                    clothesToPush.append(headgear)
                    
                if scarf!=-1:
                    clothesToPush.append(scarf)
                    
                if glove!=-1:
                    clothesToPush.append(glove)
                    
                if bonnet!=-1:
                    clothesToPush.append(bonnet)
                    
                if hood!=-1:
                    clothesToPush.append(hood)
                    
                if foulard!=-1:
                    clothesToPush.append(foulard)
                    
                if cravat!=-1:
                    clothesToPush.append(cravat)
                    
                if bag!=-1:
                    clothesToPush.append(bag)

                outfit.various.set(clothesToPush)
                outfit.nbrLayer = outfitLayers
                #outfit.temp = temp
                outfit.ptsTop = ptsTop
                outfit.ptsPant = ptsPant
                outfit.ptsCoat = ptsCoat
                outfit.ptsShoes = ptsShoes
                outfit.ptsVarious = ptsVarious
                outfit.weather = weatherDescription
                outfit.save()
                
                
                
                success = True
            else: # si form non valide
                data['message'] = 'Formulaire non valide.'

        else: #si non post

            ####################
            form = OutfitGenerationForm()
            #return render(request, 'dressingManage/generateOutfit.html', locals())
            ####################

            data['message'] = 'Une requête POST est nécessaire.'


    else:
        return HttpResponseForbidden('Utilisateur non authentifié')

    data['success'] = success
    return HttpResponse(json.dumps(data), content_type='application/json')


def switchClothe(request, idC, way):
    data = {}
    success = False
    currentUser = request.user
    lColIds = []
    lColPantIds = []
    flagSecond = flagFirst = flagPant = flagShoes = flagCoat = flagUnderwear = flagUnderwearTop = flagSock = 0
   
    clothToReturn = -1

    if currentUser.is_authenticated():
        outfit = get_object_or_404(Outfit, userOwner = currentUser)

        '''for c in outfit.clothes.all():
            
            if c.category.area == 2: # si pantalon
                lColPant = c.colors
                for col in lColPant.all():
                    quant = Quantity.objects.get(id = c.quantities.all(), color = col)

                    if quant.quantity >= 20:   
                        if col.id == 1 or col.id == 2: # si noir ou blanc 
                            if len(lColIds) == 0: # et si liste vide on ajoute tout
                                lColPantIds = list(range(1, 25))

                        else: #si pas noir ni blc
                            pat = Pattern.objects.get(id = col.id) # on récupère le pattern correspondant
                            if len(lColPantIds) == 0: # si liste vide on ajoute les couleurs
                                for color in pat.colors.all():
                                    lColPantIds.append(color.id)
                            else: # sinon on ajoute les couleurs
                                for color in pat.colors.all():
                                    lColPantIds.append(color.id)
                
            if c.id != int(idC):
                lCol = c.colors
                for col in lCol.all():
                    quant = Quantity.objects.get(id = c.quantities.all(), color = col)

                    if quant.quantity >= 20:   
                        if col.id == 1 or col.id == 2: # si noir ou blanc 
                            if len(lColIds) == 0: # et si liste vide on ajoute tout
                                lColIds = list(range(1, 25))

                        else: #si pas noir ni blc
                            pat = Pattern.objects.get(id = col.id) # on récupère le pattern correspondant
                            if len(lColIds) == 0: # si liste vide on ajoute les couleurs
                                for color in pat.colors.all():
                                    lColIds.append(color.id)
                            else: # sinon on ajoute les couleurs 
                                for color in pat.colors.all():
                                    lColIds.append(color.id)'''
        #second
        if outfit.secondLayer and outfit.secondLayer.id == int(idC):
            flagSecond = 1
        else:
            for col in outfit.secondLayer.colors.all():
                quant = Quantity.objects.get(id = outfit.secondLayer.quantities.all(), color = col)

                if quant.quantity >= 20:   
                    if col.id == 1 or col.id == 2: # si noir ou blanc 
                        if len(lColIds) == 0: # et si liste vide on ajoute tout
                            lColIds = list(range(1, 25))

                    else: #si pas noir ni blc
                        pat = Pattern.objects.get(id = col.id) # on récupère le pattern correspondant
                        if len(lColIds) == 0: # si liste vide on ajoute les couleurs
                            for color in pat.colors.all():
                                lColIds.append(color.id)
                        else: # sinon on ajoute les couleurs 
                            for color in pat.colors.all():
                                lColIds.append(color.id)

        #first
        if outfit.firstLayer and outfit.firstLayer.id == int(idC):
            flagFirst = 1
        else:
            for col in outfit.firstLayer.colors.all():
                quant = Quantity.objects.get(id = outfit.firstLayer.quantities.all(), color = col)

                if quant.quantity >= 20:   
                    if col.id == 1 or col.id == 2: # si noir ou blanc 
                        if len(lColIds) == 0: # et si liste vide on ajoute tout
                            lColIds = list(range(1, 25))

                    else: #si pas noir ni blc
                        pat = Pattern.objects.get(id = col.id) # on récupère le pattern correspondant
                        if len(lColIds) == 0: # si liste vide on ajoute les couleurs
                            for color in pat.colors.all():
                                lColIds.append(color.id)
                        else: # sinon on ajoute les couleurs 
                            for color in pat.colors.all():
                                lColIds.append(color.id)


        #pant
        if outfit.pant and outfit.pant.id == int(idC):
            flagPant = 1
        else:
            #pour gérer le switch du manteau
            lColPant = outfit.pant.colors
            for col in lColPant.all():
                quant = Quantity.objects.get(id = outfit.pant.quantities.all(), color = col)

                if quant.quantity >= 20:   
                    if col.id == 1 or col.id == 2: # si noir ou blanc 
                        if len(lColIds) == 0: # et si liste vide on ajoute tout
                            lColPantIds = list(range(1, 25))

                    else: #si pas noir ni blc
                        pat = Pattern.objects.get(id = col.id) # on récupère le pattern correspondant
                        if len(lColPantIds) == 0: # si liste vide on ajoute les couleurs
                            for color in pat.colors.all():
                                lColPantIds.append(color.id)
                        else: # sinon on ajoute les couleurs
                            for color in pat.colors.all():
                                lColPantIds.append(color.id)

                                    
            for col in outfit.firstLayer.colors.all():
                quant = Quantity.objects.get(id = outfit.firstLayer.quantities.all(), color = col)

                if quant.quantity >= 20:   
                    if col.id == 1 or col.id == 2: # si noir ou blanc 
                        if len(lColIds) == 0: # et si liste vide on ajoute tout
                            lColIds = list(range(1, 25))

                    else: #si pas noir ni blc
                        pat = Pattern.objects.get(id = col.id) # on récupère le pattern correspondant
                        if len(lColIds) == 0: # si liste vide on ajoute les couleurs
                            for color in pat.colors.all():
                                lColIds.append(color.id)
                        else: # sinon on ajoute les couleurs 
                            for color in pat.colors.all():
                                lColIds.append(color.id)


        #shoes
        if outfit.shoes and outfit.shoes.id == int(idC):
            flagShoes = 1
        else:
            for col in outfit.firstLayer.colors.all():
                quant = Quantity.objects.get(id = outfit.firstLayer.quantities.all(), color = col)

                if quant.quantity >= 20:   
                    if col.id == 1 or col.id == 2: # si noir ou blanc 
                        if len(lColIds) == 0: # et si liste vide on ajoute tout
                            lColIds = list(range(1, 25))

                    else: #si pas noir ni blc
                        pat = Pattern.objects.get(id = col.id) # on récupère le pattern correspondant
                        if len(lColIds) == 0: # si liste vide on ajoute les couleurs
                            for color in pat.colors.all():
                                lColIds.append(color.id)
                        else: # sinon on ajoute les couleurs 
                            for color in pat.colors.all():
                                lColIds.append(color.id)


        #coat
        if outfit.coat and outfit.coat.id == int(idC):
            flagCoat = 1
        else:
            for col in outfit.firstLayer.colors.all():
                quant = Quantity.objects.get(id = outfit.firstLayer.quantities.all(), color = col)

                if quant.quantity >= 20:   
                    if col.id == 1 or col.id == 2: # si noir ou blanc 
                        if len(lColIds) == 0: # et si liste vide on ajoute tout
                            lColIds = list(range(1, 25))

                    else: #si pas noir ni blc
                        pat = Pattern.objects.get(id = col.id) # on récupère le pattern correspondant
                        if len(lColIds) == 0: # si liste vide on ajoute les couleurs
                            for color in pat.colors.all():
                                lColIds.append(color.id)
                        else: # sinon on ajoute les couleurs 
                            for color in pat.colors.all():
                                lColIds.append(color.id)



        #underwear
        if outfit.underwear and outfit.underwear.id == int(idC):
            flagUnderwear = 1
        
        #underwearTop
        if outfit.underwearTop and outfit.underwearTop.id == int(idC):
            flagUnderwearTop = 1

        #socks
        if outfit.sock and outfit.sock.id == int(idC):
            flagSock = 1


                  
            
        counts = Counter(lColIds)
        lColIds = [value for value, count in counts.items() if count > 1]
        lColIds.append(1)
        lColIds.append(2)
        lColIds = list(set(lColIds))



        ptsTop = outfit.ptsTop
        ptsPant = outfit.ptsPant 
        ptsCoat = outfit.ptsCoat 
        ptsShoes = outfit.ptsShoes
        ptsVarious = outfit.ptsVarious 

        if outfit.nbrLayer == 2:
            ptsFirst = int(ptsTop/3)
            ptsSecond = ptsTop - ptsFirst

        

        if flagSecond == 1:
            #on récupère tous les vêt qui sont potentiellement compatibles
            lSecondLayer = Clothe.objects.filter(Q(user = currentUser) & Q(themes = outfit.theme) & Q(category__area = 1) & Q(colors__id__in = lColIds) & (Q(category__layer = 2) | Q(category__layer = 0)) & Q(id != outfit.firstLayer.id))
            lSecondLayerIds = []
            if lSecondLayer:
                #on ne selectionne que ceux qui match avec la temp
                for c in lSecondLayer:
                    warmthTot = c.category.warmth * c.warmth
                    if (warmthTot >= (ptsSecond-1)) and (warmthTot <= (ptsSecond+1)):
                        lSecondLayerIds.append(c.id)


                if len(lSecondLayerIds) == 0:
                    clothToReturn = -1
                else:
                    #si tout est OK, on parcourt le dic et lorsqu'on trouve le vet qui est actuellement porté, on + ou - 1 selon le senspassé en param
                    for clothe in lSecondLayerIds:
                        if clothe == int(idC):
                            if int(way) == 0:
                                if lSecondLayerIds.index(clothe)-1 < 0:
                                    clothToReturn = lSecondLayerIds[len(lSecondLayerIds)-1]
                                else:
                                    clothToReturn = lSecondLayerIds[lSecondLayerIds.index(clothe)-1]
                            else:
                                if lSecondLayerIds.index(clothe)+1 > len(lSecondLayerIds-1):
                                    clothToReturn = lSecondLayerIds[0]
                                else:
                                    clothToReturn = lSecondLayerIds[lSecondLayerIds.index(clothe)+1]
            else:
                clothToReturn = -1
            newCloth = Clothe.objects.get(id = clothToReturn)
            outfit.secondLayer.set(newCloth)


        if flagFirst == 1:
            #on récupère tous les vêt qui sont potentiellement compatibles
            if outfit.nbrLayer == 2:
                lFirstLayer = Clothe.objects.filter(Q(user = currentUser) & Q(themes = outfit.theme) & Q(category__area = 1) & Q(colors__id__in = lColIds) & (Q(category__layer = 1) | Q(category__layer = 0)) & Q(id != outfit.secondLayer.id))
            else:
                ptsFirst = ptsTop
                lFirstLayer = Clothe.objects.filter(Q(user = currentUser) & Q(themes = outfit.theme) & Q(category__area = 1) & Q(colors__id__in = lColIds) & (Q(category__layer = 1) | Q(category__layer = 0)))

                
            if lFirstLayer:
                lFirstLayerIds = []
                #on ne selectionne que ceux qui match avec la temp
                for c in lFirstLayer:
                    warmthTot = c.category.warmth * c.warmth
                    if (warmthTot >= (ptsFirst-1)) and (warmthTot <= (ptsFirst+1)):
                        lFirstLayerIds.append(c.id)


                if len(lFirstLayerIds) == 0:
                    clothToReturn = -1
                else:
                    #si tout est OK, on parcourt le dic et lorsqu'on trouve le vet qui est actuellement porté, on + ou - 1 selon le senspassé en param
                    for clothe in lFirstLayerIds:
                        if clothe == int(idC):
                            if int(way) == 0:
                                if lFirstLayerIds.index(clothe)-1 < 0:
                                    clothToReturn = lFirstLayerIds[len(lFirstLayerIds)-1]
                                else:
                                    clothToReturn = lFirstLayerIds[lFirstLayerIds.index(clothe)-1]
                            else:
                                if lFirstLayerIds.index(clothe)+1 > len(lFirstLayerIds)-1:
                                    clothToReturn = lFirstLayerIds[0]
                                else:
                                    clothToReturn = lFirstLayerIds[lFirstLayerIds.index(clothe)+1]
            else:
                clothToReturn = -1
                        


        #pantalon
        if flagPant == 1:
            lPantIds = []
            lPant = Clothe.objects.filter(Q(user = currentUser) & Q(themes = outfit.theme) & Q(category__area = 2) & (Q(colors__id__in = lColIds) | Q(category__id = 31)))

            if lPant:
                for c in lPant:
                    warmthTot = c.category.warmth * c.warmth
                    if (warmthTot >= (ptsPant-1)) and (warmthTot <= (ptsPant+1)):
                        lPantIds.append(c.id)

                if len(lPantIds) == 0:
                    clothToReturn = -1
                else:
                    for clothe in lPantIds:
                        if clothe == int(idC):
                            if int(way) == 0:
                                if lPantIds.index(clothe)-1 < 0:
                                    clothToReturn = lPantIds[len(lPantIds)-1]
                                else:
                                    clothToReturn = lPantIds[lPantIds.index(clothe)-1]
                            else:
                                if lPantIds.index(clothe)+1 > len(lPantIds)-1:
                                    clothToReturn = lPantIds[0]
                                else:
                                    clothToReturn = lPantIds[lPantIds.index(clothe)+1]
            else:
                clothToReturn = -1


        #chaussures
        if flagShoes == 1:
            if SecondLayer.id == 10: # si veste costume
                lShoes = Clothe.objects.filter(Q(user = currentUser) & Q(themes = outfit.theme) & Q(category__area = 3) & (Q(category__layer = 50) | Q(category__layer = 39) | Q(category__layer = 40)) & Q(colors__id__in = lColIds))
                if lShoes:
                    lShoesIds = [c.id for c in lShoes]
                    
                    for clothe in lShoesIds:
                        if shoes == int(idC):
                            if int(way) == 0:
                                if lShoesIds.index(clothe)-1 < 0:
                                    clothToReturn = lShoesIds[len(lShoesIds)-1]
                                else:
                                    clothToReturn = lShoesIds[lShoesIds.index(clothe)-1]
                            else:
                                if lShoesIds.index(clothe)+1 > len(lShoesIds)-1:
                                    clothToReturn = lShoesIds[0]
                                else:
                                    clothToReturn = lShoesIds[lShoesIds.index(clothe)+1]
                else:
                    clothToReturn = -1

            else: # si pas veste
                lShoes = Clothe.objects.filter(Q(user = currentUser) & Q(themes = outfit.theme) & Q(category__area = 3) & Q(colors__id__in = lColIds))
                if lShoes:
                    for c in lShoes:
                        warmthTot = c.category.warmth * c.warmth
                        if (warmthTot >= (ptsShoes-1)) and (warmthTot <= (ptsShoes+1)):
                            lShoesIds.append(c.id)

                    if len(lShoesIds) == 0:
                        clothToReturn = -1
                    else:
                        for clothe in lShoesIds:
                            if clothe == int(idC):
                                if int(way) == 0:
                                    if lShoesIds.index(clothe)-1 < 0:
                                        clothToReturn = lShoesIds[len(lShoesIds)-1]
                                    else:
                                        clothToReturn = lShoesIds[lShoesIds.index(clothe)-1]
                                else:
                                    if lShoesIds.index(clothe)+1 > len(lShoesIds)-1:
                                        clothToReturn = lShoesIds[0]
                                    else:
                                        clothToReturn = lShoesIds[lShoesIds.index(clothe)+1]
                else:
                    clothToReturn = -1



        #manteau
        if flagCoat == 1:
            
            lCoatIds = []
            
            if len(lColPantIds) != 0:
                lColIdsCoat = [c for c in list(lColIds) if c not in lColPantIds]
                lColIdsCoat.append(1)
                lColIdsCoat.append(2)
                lColIdsCoat = list(set(lColIdsCoat))
            else:
                lColIdsCoat = lColIds

            lCoat = Clothe.objects.filter(Q(user = currentUser) & Q(themes = outfit.theme) & Q(category__area = 1) & Q(category__layer = 3) & Q(colors__id__in = lColIds))
            
            if lCoat:
                
                for c in lCoat:
                    warmthTot = c.category.warmth * c.warmth
                    if (warmthTot >= (ptsCoat-3)) and (warmthTot <= (ptsCoat+3)):
                        lCoatIds.append(c.id)
                        
                if len(lCoatIds) == 0:
                    clothToReturn = -1
                else:
                    for clothe in lCoatIds:
                        if clothe == int(idC):
                            if int(way) == 0:
                                if lCoatIds.index(clothe)-1 < 0:
                                    clothToReturn = lCoatIds[len(lCoatIds)-1]
                                else:
                                    clothToReturn = lCoatIds[lCoatIds.index(clothe)-1]
                            else:
                                if lCoatIds.index(clothe)+1 > len(lCoatIds)-1:
                                    clothToReturn = lCoatIds[0]
                                else:
                                    clothToReturn = lCoatIds[lCoatIds.index(clothe)+1]
                                    
            else:
                clothToReturn = -1




        #ss vêt
        if flagUnderwear == 1:    
            lUnderwear = Clothe.objects.filter(Q(user = currentUser) & Q(themes = outfit.theme) & Q(category__area = 4) & (Q(category__id = 58) | Q(category__id = 57) | Q(category__id = 56) | Q(category__id = 55) | Q(category__id = 54) | Q(category__id = 53)))

            if lUnderwear:
                lUnderwearIds = [c.id for c in lUnderwear]
                for clothe in lUnderwearIds:
                    if clothe == int(idC):
                        if int(way) == 0:
                            if lUnderwearIds.index(clothe)-1 < 0:
                                clothToReturn = lUnderwearIds[len(lUnderwearIds)-1]
                            else:
                                clothToReturn = lUnderwearIds[lUnderwearIds.index(clothe)-1]
                        else:
                            if lUnderwearIds.index(clothe)+1 > len(lUnderwearIds)-1:
                                clothToReturn = lUnderwearIds[0]
                            else:
                                clothToReturn = lUnderwearIds[lUnderwearIds.index(clothe)+1]
            else:
                clothToReturn = -1


        #ss vêt top
        if flagUnderwearTop == 1:
            
            lUnderwearTop = Clothe.objects.filter(Q(user = currentUser) & Q(themes = outfit.theme) & Q(category__area = 4) & (Q(category__id = 64) | Q(category__id = 59)))

            if lUnderwearTop:
                lUnderwearTopIds = [c.id for c in lUnderwearTop]
                for clothe in lUnderwearTopIds:
                    if clothe == int(idC):
                        if int(way) == 0:
                            if lUnderwearTopIds.index(clothe)-1 < 0:
                                clothToReturn = lUnderwearTopIds[len(lUnderwearTopIds)-1]
                            else:
                                clothToReturn = lUnderwearTopIds[lUnderwearTopIds.index(clothe)-1]
                        else:
                            if lUnderwearTopIds.index(clothe)+1 > len(lUnderwearTopIds)-1:
                                clothToReturn = lUnderwearTopIds[0]
                            else:
                                clothToReturn = lUnderwearTopIds[lUnderwearTopIds.index(clothe)+1]
            else:
                clothToReturn = -1


        #chaussettes
        if flagSock == 1:     
            lSocks = Clothe.objects.filter(Q(user = currentUser) & Q(themes = outfit.theme) & Q(category__area = 4) & (Q(category__id = 63) | Q(category__id = 62) | Q(category__id = 61) | Q(category__id = 60)))

            if lSocks:
                lSockIds = [c.id for c in lSocks]
                for clothe in lSockIds:
                    if clothe == int(idC):
                        if int(way) == 0:
                            if lSockIds.index(clothe)-1 < 0:
                                clothToReturn = lSockIds[len(lSockIds)-1]
                            else:
                                clothToReturn = lSockIds[lSockIds.index(clothe)-1]
                        else:
                            if lSockIds.index(clothe)+1 > len(lSockIds)-1:
                                clothToReturn = lSockIds[0]
                            else:
                                clothToReturn = lSockIds[lSockIds.index(clothe)+1]
            else:
                clothToReturn = -1
                    


        cloth = Clothe.objects.get(id = int(idC))
        area = cloth.category.area
        
        #casquette
        if area == 5 and cloth.category.id == 69:
            
            lCap = Clothe.objects.filter(Q(user = currentUser) & Q(themes = outfit.theme) & Q(category__area = 5) & Q(category__id = 69))

            if lCap:
                lCapIds = [c.id for c in lCap]
                for clothe in lCapIds:
                    if clothe == int(idC):
                        if int(way) == 0:
                            if lCapIds.index(clothe)-1 < 0:
                                clothToReturn = lCapIds[len(lCapIds)-1]
                            else:
                                clothToReturn = lCapIds[lCapIds.index(clothe)-1]
                        else:
                            if lCapIds.index(clothe)+1 > len(lCapIds)-1:
                                clothToReturn = lCapIds[0]
                            else:
                                clothToReturn = lCapIds[lCapIds.index(clothe)+1]
            else:
                clothToReturn = -1



        #chapeau et beret
        if area == 5 and (cloth.category.id == 68 or cloth.category.id == 70):
            
            lHeadgear = Clothe.objects.filter(Q(user = currentUser) & Q(themes = outfit.theme) & Q(category__area = 5) & (Q(category__id = 68) | Q(category__id = 70)))

            if lHeadgear:
                lHeadgearIds = [c.id for c in lHeadgear]
                for clothe in lHeadgearIds:
                    if clothe == int(idC):
                        if int(way) == 0:
                            if lHeadgearIds.index(clothe)-1 < 0:
                                clothToReturn = lHeadgearIds[len(lHeadgearIds)-1]
                            else:
                                clothToReturn = lHeadgearIds[lHeadgearIds.index(clothe)-1]
                        else:
                            if lHeadgearIds.index(clothe)+1 > len(lHeadgearIds)-1:
                                clothToReturn = lHeadgearIds[0]
                            else:
                                clothToReturn = lHeadgearIds[lHeadgearIds.index(clothe)+1]
            else:
                clothToReturn = -1



        #echarpe
        if area == 5 and cloth.category.id == 65:
            
            lScarf = Clothe.objects.filter(Q(user = currentUser) & Q(themes = outfit.theme) & Q(category__area = 5) & Q(category__id = 65))

            if lScarf:
                lScarfIds = [c.id for c in lScarf]
                for clothe in lScarfIds:
                    if clothe == int(idC):
                        if int(way) == 0:
                            if lScarfIds.index(clothe)-1 < 0:
                                clothToReturn = lScarfIds[len(lScarfIds)-1]
                            else:
                                clothToReturn = lScarfIds[lScarfIds.index(clothe)-1]
                        else:
                            if lScarfIds.index(clothe)+1 > len(lScarfIds)-1:
                                clothToReturn = lScarfIds[0]
                            else:
                                clothToReturn = lScarfIds[lScarfIds.index(clothe)+1]
            else:
                clothToReturn = -1
                


        #gants et mitaines
        if area == 5 and (cloth.category.id == 66 or cloth.category.id == 72):
            
            lGlove = Clothe.objects.filter(Q(user = currentUser) & Q(themes = outfit.theme) & Q(category__area = 5) & (Q(category__id = 66) | Q(category__id = 72)))

            if lGlove:
                lGloveIds = [c.id for c in lGlove]
                for clothe in lGloveIds:
                    if clothe == int(idC):
                        if int(way) == 0:
                            if lGloveIds.index(clothe)-1 < 0:
                                clothToReturn = lGloveIds[len(lGloveIds)-1]
                            else:
                                clothToReturn = lGloveIds[lGloveIds.index(clothe)-1]
                        else:
                            if lGloveIds.index(clothe)+1 > len(lGloveIds)-1:
                                clothToReturn = lGloveIds[0]
                            else:
                                clothToReturn = lGloveIds[lGloveIds.index(clothe)+1]
            else:
                clothToReturn = -1



        #bonnet
        if area == 5 and cloth.category.id == 67:
            
            lBonnet = Clothe.objects.filter(Q(user = currentUser) & Q(themes = outfit.theme) & Q(category__area = 5) & Q(category__id = 67))

            if lBonnet:
                lBonnetIds = [c.id for c in lBonnet]
                for clothe in lBonnetIds:
                    if clothe == int(idC):
                        if int(way) == 0:
                            if lBonnetIds.index(clothe)-1 < 0:
                                clothToReturn = lBonnetIds[len(lBonnetIds)-1]
                            else:
                                clothToReturn = lBonnetIds[lBonnetIds.index(clothe)-1]
                        else:
                            if lBonnetIds.index(clothe)+1 > len(lBonnetIds)-1:
                                clothToReturn = lBonnetIds[0]
                            else:
                                clothToReturn = lBonnetIds[lBonnetIds.index(clothe)+1]
            else:
                clothToReturn = -1



        #cagoule
        if area == 5 and cloth.category.id == 71:
            
            lHood = Clothe.objects.filter(Q(user = currentUser) & Q(themes = outfit.theme) & Q(category__area = 5) & Q(category__id = 71))

            if lHood:
                lHoodIds = [c.id for c in lHood]
                for clothe in lHoodIds:
                    if clothe == int(idC):
                        if int(way) == 0:
                            if lHoodIds.index(clothe)-1 < 0:
                                clothToReturn = lHoodIds[len(lHoodIds)-1]
                            else:
                                clothToReturn = lHoodIds[lHoodIds.index(clothe)-1]
                        else:
                            if lHoodIds.index(clothe)+1 > len(lHoodIds)-1:
                                clothToReturn = lHoodIds[0]
                            else:
                                clothToReturn = lHoodIds[lHoodIds.index(clothe)+1]
            else:
                clothToReturn = -1



        #etole foulard
        if area == 5 and (cloth.category.id == 74 or cloth.category.id == 73):
            
            lFoulard = Clothe.objects.filter(Q(user = currentUser) & Q(themes = outfit.theme) & Q(category__area = 5) & (Q(category__id = 74) | Q(category__id = 73)))

            if lFoulard:
                lFoulardIds = [c.id for c in lFoulard]
                for clothe in lFoulardIds:
                    if clothe == int(idC):
                        if int(way) == 0:
                            if lFoulardIds.index(clothe)-1 < 0:
                                clothToReturn = lFoulardIds[len(lFoulardIds)-1]
                            else:
                                clothToReturn = lFoulardIds[lFoulardIds.index(clothe)-1]
                        else:
                            if lFoulardIds.index(clothe)+1 > len(lFoulardIds)-1:
                                clothToReturn = lFoulardIds[0]
                            else:
                                clothToReturn = lFoulardIds[lFoulardIds.index(clothe)+1]
            else:
                clothToReturn = -1




        #noeud pap / cravate
        if area == 5 and (cloth.category.id == 75 or cloth.category.id == 76):
            
            lCravat = Clothe.objects.filter(Q(user = currentUser) & Q(themes = outfit.theme) & Q(category__area = 5) & Q(colors__id__in = lColIds) & (Q(category__id = 75) | Q(category__id = 76)))

            if lCravat:
                lCravatIds = [c.id for c in lCravat]
                for clothe in lCravatIds:
                    if clothe == int(idC):
                        if int(way) == 0:
                            if lCravatIds.index(clothe)-1 < 0:
                                clothToReturn = lCravatIds[len(lCravatIds)-1]
                            else:
                                clothToReturn = lCravatIds[lCravatIds.index(clothe)-1]
                        else:
                            if lCravatIds.index(clothe)+1 > len(lCravatIds)-1:
                                clothToReturn = lCravatIds[0]
                            else:
                                clothToReturn = lCravatIds[lCravatIds.index(clothe)+1]
            else:
                clothToReturn = -1


        #sac
        if area == 5 and (cloth.category.id == 77 or cloth.category.id == 78 or cloth.category.id == 79):
            
            lBag = Clothe.objects.filter(Q(user = currentUser) & Q(themes = outfit.theme) & Q(category__area = 1) & Q(colors__id__in = lColIds) & (Q(category__id = 77) | Q(category__id = 78) | Q(category__id = 79)))

            if lBag:
                lBagIds = [c.id for c in lBag]
                for clothe in lBagIds:
                    if clothe == int(idC):
                        if int(way) == 0:
                            if lBagIds.index(clothe)-1 < 0:
                                clothToReturn = lBagIds[len(lBagIds)-1]
                            else:
                                clothToReturn = lBagIds[lBagIds.index(clothe)-1]
                        else:
                            if lBagIds.index(clothe)+1 > len(lBagIds)-1:
                                clothToReturn = lBagIds[0]
                            else:
                                clothToReturn = lBagIds[lBagIds.index(clothe)+1]
            else:
                clothToReturn = -1

                
        info = {}

        if clothToReturn != -1:
            info['id'] = clothToReturn
            newCloth = Clothe.objects.get(id = clothToReturn)
            info['photo'] = newCloth.photo
            data['clothe'] = info

            if flagSecond == 1:
                outfit.secondLayer = newCloth
            elif flagFirst == 1:
                outfit.firstLayer = newCloth
            elif flagPant == 1:
                outfit.pant = newCloth
            elif flagShoes == 1:
                outfit.shoes = newCloth
            elif flagCoat == 1:
                outfit.coat = newCloth
            elif flagUnderwear == 1:
                outfit.underwear = newCloth
            elif flagUnderwearTop == 1:
                outfit.underwearTop = newCloth
            elif flagSock == 1:
                outfit.sock = newCloth
            else:
                outfit.various.add(newCloth)
                outfit.various.remove(cloth)
                
            outfit.save()
            success = True
        else:
            data['success'] = success
            data['message'] = "Erreur lors de la récupération du vêtement"
        
        
            
    else:
        return HttpResponseForbidden('Utilisateur non authentifié')

    data['success'] = success
    return HttpResponse(json.dumps(data), content_type='application/json')



