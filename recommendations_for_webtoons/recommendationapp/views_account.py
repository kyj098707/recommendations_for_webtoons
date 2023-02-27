from django.shortcuts import render,redirect
from django.contrib import auth,messages
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from .helper import send_mail
from django.core.exceptions import ValidationError
from .models import *
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator


"""def account_test(request):
    user = request.user
    # 로그인되어 있으면 바로 보내기
    if user.is_authenticated:
        print(str(user.email))
        return render(request,'./_02_service/main.html')
"""    

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
                return redirect('rcmd:service')
            else:
                return render(request,"login.html",{"error:username or password is incorrect"})
    return render(request,'_00_account/account.html')



def activate(request, uid64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        current_user = Member.objects.get(uid=uid)
        print("@@@@@@@@@@")
    except (TypeError, ValueError, OverflowError, Member.DoesNotExist, ValidationError):
        print("###############")
        messages.error(request, '메일 인증에 실패했습니다.')
        
        return redirect('rcmd:login')

    if default_token_generator.check_token(current_user, token):
        current_user.is_active = True
        current_user.save()

        messages.info(request, '메일 인증이 완료 되었습니다. 회원가입을 축하드립니다!')
        return redirect('rcmd:login')

    messages.error(request, '메일 인증에 실패했습니다.')
    return redirect('rcmd:login')


def sendmsg_test(request):
    user = request.user
    print(user.pk)
    send_mail(
        '{}님의 회원가입 인증메일 입니다.'.format(user.uid),
        [user.email],
        html=render_to_string('_00_account/email.html', {
            'user': user,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).encode().decode(),
            'domain': 'naver',
            'token': default_token_generator.make_token(user),
        }),
    )
    return redirect('rcmd:intro')


def logout_test(request):
    auth.logout(request)
    return redirect('rcmd:intro')