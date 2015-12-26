from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login
from userManage.forms import AddForm
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
            #new_user = User(username = new_username, password = new_password)
            #new_user.save()

            user = User.objects.create_user(new_username, new_mail, new_password)
            
            data = {'new_user':user.username}
    else:
        form = AddForm()

    
    #return render(request, 'userManage/add.html', locals())
    return HttpResponse(json.dumps(data), content_type='application/json')

#def delete(request):
