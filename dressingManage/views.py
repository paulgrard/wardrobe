# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, Http404
from dressingManage.forms import AddClotheForm, AddThemeForm, GetThemeForm, forms, WeatherForm, EditClotheForm
from django.contrib.auth.models import User
from dressingManage.models import Clothe, Category, Color, Theme, Quantity
import json, os
from urllib.request import urlopen
from django.core.files.uploadedfile import TemporaryUploadedFile
from wardrobe.settings import IMG_FOLDER

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
                            thm = Theme.objects.get(id = int(i), userOwner=request.user)
                            newClothe.themes.add(thm)
                        except Theme.DoesNotExist:
                            data['success'] = False
                            data['message'] = 'Un des thèmes n\'existe pas.'

                            return HttpResponse(json.dumps(data), content_type='application/json')

                #for valColor in colorsC:
                if len(colorsC)>3 or len(quantitiesC)>3:
                    data['success'] = False
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


                cloth = get_object_or_404(Clothe, id = idC, user=currentUser)

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
                            themes.append(Theme.objects.get(id = int(i), userOwner=request.user))
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



def getClothesFromCategory(request, idC):
    data = {}
    success = False
    clothes = []
    pKey = []
    currentUser = request.user
    if currentUser.is_authenticated():
        categ = get_object_or_404(Category, pk = idC)
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
<<<<<<< HEAD

=======

        themesFromNullUser = Theme.objects.filter(userOwner = None)
        for themeNull in themesFromNullUser:
            themes.append(themeNull.name)
            idTheme.append(themeNull.id)

>>>>>>> ff1ce98ae2e26b25d500ac3ea9cd757e5b374677
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
<<<<<<< HEAD

=======
    temp = {}

>>>>>>> ff1ce98ae2e26b25d500ac3ea9cd757e5b374677
    if currentUser.is_authenticated():
        clothing = get_object_or_404(Clothe, id = idC, user = currentUser)
        if clothing:
            colorsFromClothe = clothing.colors
            quantFromClothe = clothing.quantities

            for c in colorsFromClothe.all():
<<<<<<< HEAD
                colors.append(c.code)

=======
                quanti = []
                temp['code'] = c.code
                for q in quantFromClothe.all():
                    quant = Quantity.objects.get(id = q.id, color = c)
                    quanti.append(quant.quantity)

                temp['quantity'] = quanti

                colors.append(temp)

>>>>>>> ff1ce98ae2e26b25d500ac3ea9cd757e5b374677
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

        cats = Category.objects.filter(area = idA)
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
        cloth = Clothe.objects.get(id = idC, user=currentUser)
        cloth.state = state
        cloth.save()
        success = True

    else:
        return HttpResponseForbidden('Utilisateur non authentifié')

    data['success'] = success
    return HttpResponse(json.dumps(data), content_type='application/json')


