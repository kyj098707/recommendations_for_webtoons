from django.shortcuts import render,redirect
from django.contrib import auth
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout

from .models import *

def account_test(request):
    user = request.user
    if user.is_authenticated:
        return HttpResponse("You are already authenticated as " + str(user.email))
    ### db 겹치면 안되는 부분에 대해서 예외처리 필요
    if request.POST:
        if request.POST['btn'] == 'signup':
            if request.POST['password1'] == request.POST['password2']:
                email = request.POST['email']
                username = request.POST['username']
                password = request.POST['password1']
                member = Member.objects.create_user(email=email,username=username, password=password)
                nickname, gender, age = request.POST['nickname'], request.POST['gender'], request.POST['age']
                gender = 0 if gender == '남' else 1
                user = Member.objects.get(email=email)
                userprofile = Userprofile.objects.create(member=user,nickname=nickname, gender=gender,age=age)
                userprofile.save()
                return render(request,'_00_account/account.html')
        if request.POST['btn'] == 'login':
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email,password=password)
            if user:
                auth.login(request, user)
                return render(request,'./_02_service/main.html')
            else:
                return render(request,"login.html",{"error:username or password is incorrect"})
    return render(request,'_00_account/account.html')

def logout_test(request):
    auth.logout(request)
    return render(request, "./_00_account/login.html")