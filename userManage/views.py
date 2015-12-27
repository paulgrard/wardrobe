from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, logout
from userManage.forms import AddForm, forms
from django.contrib.auth.models import User
import json
# Create your views here.

def add(request):
    data = []
    if request.method == "POST":
        form = AddForm(request.POST)
        if form.is_valid():
            new_username = form.cleaned_data["username"]
            new_mail = form.cleaned_data["mail"]
            new_password = form.cleaned_data["password"]
            if User.objects.filter(email=new_mail).exists() or User.objects.filter(username=new_username).exists():
                data = {'new_user':'This email or username is already used'}
            else:
                user = User.objects.create_user(username=new_username, email=new_mail, password=new_password)
                if user:
                    data = {'new_user':user.username}
                else:
                    data = {'new_user':'Error during creation of user'}
    else:
        form = AddForm()

    return render(request, 'userManage/add.html', locals())
    return HttpResponse(json.dumps(data), content_type='application/json')



def deactivate(request):
    data = []
    flag = False
    
    if request.user.is_authenticated():
        userToDeactivate = request.user
        if userToDeactivate.is_active:
            userToDeactivate.is_active=False
            userToDeactivate.save()
            data = {'userDeactivated':userToDeactivate.username}
            logout(request)
        else:
            data = {'userDeactivated':'User already deactivated'}
            #print('User already deactivated')
    else:
        data = {'userDeactivated':'User not authenticated'}
        #print('User not authenticated')

    #return render(request, 'userManage/deactivate.html', locals())
    return HttpResponse(json.dumps(data), content_type='application/json')
