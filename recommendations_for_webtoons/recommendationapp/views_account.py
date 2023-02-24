from django.shortcuts import render,redirect
from django.contrib import auth

from .models import *


def signup_test(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['confirm']:
            print(request.POST['email'])
            user = Member.objects.create_user(email=request.POST['email'],password=request.POST['password'])
            auth.login(request,user)
            return redirect('/')
    return render(request, "./_00_account/signup.html")

def login_test(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(request,email=email,password=password)

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