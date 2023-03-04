from django.shortcuts import render,redirect
from django.contrib import auth, messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.db import transaction
from django.core.mail import send_mail
from django.core.exceptions import PermissionDenied,ValidationError
from .models import *
import json
from datetime import datetime
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.views.decorators.csrf import csrf_exempt


def join(request):
    if request.method == 'POST' :
        data = json.loads(request.body)
        email = data['email']
        username = data['username']
        password1 = data['password1']
        password2 = data['password2']
        nickname = data['nickname']
        gender = data['gender']
        birth = data['birth']
        date_birth = datetime.strptime(birth, '%Y-%m-%d')
        gender = True if gender == '1' else False if gender == '0' else None
        
        if password1 != password2 :
            result = {'response': "error"}
            return JsonResponse(result, status=200)
        elif gender == None :
            result = {'response': "error"}
            return JsonResponse(result, status=200)
    
        with transaction.atomic():
            Member.objects.create_user(email=email, username=username, password=password1)
            user = Member.objects.get(email=email)
            userprofile = Userprofile.objects.create(member=user,
                                                     nickname=nickname,
                                                     gender=gender,
                                                     date_birth=date_birth)
            userprofile.save()
        result = {'response': "complete"}
        return JsonResponse(result, status=200)

from django.contrib.auth.hashers import check_password

def log_in(request):
    if request.method == 'POST' :
        data = json.loads(request.body)
        email = data['email']
        password = data['password']
        user = authenticate(email=email, password=password)
        print(check_password(password, user.password))
        if user:
            auth.login(request, user)
            return redirect('rcmd:service')
        else:
            result = {'response': "error"}
            return JsonResponse(result, status=200)


def account_test(request):
    user = request.user
    if user.is_authenticated:
        return redirect('rcmd:service')
        # return HttpResponse("You are already authenticated as " + str(user.email))
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
                return redirect('rcmd:service')
            else:
                return render(request,"login.html",{"error:username or password is incorrect"})
    return render(request,'_00_account/account.html')


def logout_test(request):
    auth.logout(request)
    return redirect('rcmd:intro')

def push_btn(request):
    return render(request,"_00_account/btn.html")

def activate(request, uid, token):
    try:
        current_user = Member.objects.get(uid=uid)
    except (TypeError, ValueError, OverflowError, Member.DoesNotExist, ValidationError):
        messages.error(request, '메일 인증에 실패했습니다.')
        return redirect('rcmd:account')

    if default_token_generator.check_token(current_user, token):
        current_user.is_active = True
        current_user.save()

        messages.info(request, '메일 인증이 완료 되었습니다. 회원가입을 축하드립니다!')
        return redirect('rcmd:account')

    messages.error(request, '메일 인증에 실패했습니다.')
    return redirect('rcmd:account')

def sendemail(request):
    domain = "127.0.0.1:8000"
    user = Member.objects.get(email='kyj098707@gmail.com')
    uid = user.uid
    token = default_token_generator.make_token(user)

    send_mail("안녕하세요, 에이블툰입니다.",
                f"http://{domain}/activate/{uid}/{token}/",
                "kyj098707@naver.com",# 보내는 메일
                ["kyj098707@gmail.com"],# 받는 메일
                fail_silently=False)
    
"""def get_success_url(self):
    self.request.session['register_auth'] = True
    messages.success(self.request, '회원님의 입력한 Email 주소로 인증 메일이 발송되었습니다. 인증 후 로그인이 가능합니다.')
    return redirect('rcmd:intro')

def register_success(request):
    if not request.session.get('register_auth', False):
        raise PermissionDenied
    request.session['register_auth'] = False

    return render(request, 'users/register_success.html')
"""
            
              