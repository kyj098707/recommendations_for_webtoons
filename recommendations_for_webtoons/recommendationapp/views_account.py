from django.shortcuts import render,redirect
from django.contrib import auth
from django.contrib.auth.models import User

from .models import *


def signup_test(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(
                                            username=request.POST['username'],
                                            password=request.POST['password1'],
                                            email=request.POST['email'],)
            auth.login(request, user)
            return redirect('/')
        return render(request, '_00_account/signup.html')
    return render(request, '_00_account/signup.html')

def login_test(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(request,username=username,password=password)

        if user:
            print("yes user")
            auth.login(request, user)
            return redirect('/')
        else:
            print("no user")
            return render(request,"login.html",{"error:username or password is incorrect"})    
    return render(request, "./_00_account/login.html")

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('/')
    return render(request, "./_00_account/login.html")