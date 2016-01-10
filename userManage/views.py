from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth import login, logout
from userManage.forms import AddForm, forms
from django.contrib.auth.models import User
import json
# Create your views here.

def add(request):
    data = {}
    success = False
    
    if request.method == "POST":
        form = AddForm(request.POST)
        if form.is_valid():
            new_username = form.cleaned_data["username"]
            new_mail = form.cleaned_data["mail"]
            new_password = form.cleaned_data["password"]
            if User.objects.filter(email=new_mail).exists() or User.objects.filter(username=new_username).exists():
                data['message'] = 'This email or username is already used'
            else:
                user = User.objects.create_user(username=new_username, email=new_mail, password=new_password)
                if user:
                    #data = {'new_user':user.username}
                    user_co = authenticate(username=new_username, password=new_password)  # Nous vérifions si les données sont correctes
                    if user_co and user_co.is_active:  # Si l'objet renvoyé n'est pas None
                        login(request, user_co)  # nous connectons l'utilisateur
                        success = True
                    else:
                        data['message'] = 'Error during connection of the user'
                else:
                    data['message'] = 'Error during creation of the user'
                    
        else: #si form non valide
            data['message'] = 'Form not validated'
            
    else: #si non requete POST
        form = AddForm()
        data['message'] = 'Need a POST request'

    data['success'] = success
    #return render(request, 'userManage/add.html', locals())
    return HttpResponse(json.dumps(data), content_type='application/json')



def deactivate(request):
    data = {}
    success = False
    flag = False
    
    if request.user.is_authenticated():
        userToDeactivate = request.user
        if userToDeactivate.is_active:
            userToDeactivate.is_active=False
            userToDeactivate.save()
            success = True
            #data = {'userDeactivated':userToDeactivate.username}
            logout(request)
        else:
            data['message'] = 'User already deactivated'
    else:
        return HttpResponseForbidden('User is not authenticated')
        #print('User not authenticated')

    data['success'] = success
    #return render(request, 'userManage/deactivate.html', locals())
    return HttpResponse(json.dumps(data), content_type='application/json')
