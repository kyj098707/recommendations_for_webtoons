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
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

def join(request):
    if request.method == 'POST' :
        data = json.loads(request.body)
        email = data['email']
        username = data['username']
        password1 = data['password1']
        password2 = data['password2']
        nickname = data['nickname']
        gender = data['gender']
        date = f"{data['year']}-{str(data['month']).zfill(2)}-01"
        gender = True if gender == '1' else False if gender == '0' else None
        result = {'response': "error"}
        try:
            date_birth = datetime.strptime(date, '%Y-%m-%d')
        except :
            result['message'] = '날짜 형식이 올바르지 않습니다.'
            return JsonResponse(result, status=202)
        try:
            validate_email(email)
        except ValidationError as e:
            result['message'] = '이메일 형식이 올바르지 않습니다.'
            return JsonResponse(result, status=202)
        if Member.objects.filter(email=email).exists() :
            result['message'] = '이미 가입된 이메일입니다.'
            return JsonResponse(result, status=202)
        elif len(password1) < 7 :
            result['message'] = '패스워드가 너무 짧습니다.'
            return JsonResponse(result, status=202)
        elif str(password1).isdecimal() or str(password1).isalpha():
            result['message'] = '패스워드를 영문자와 숫자로 구성해주세요.'
            return JsonResponse(result, status=202)
        elif password1 != password2 :
            result['message'] = '패스워드를 확인해주세요.'
            return JsonResponse(result, status=202)
        elif len(data['year'].strip()) != 4 :
            result['message'] = '연도는 4자리로 입력해주세요.'
            return JsonResponse(result, status=202)
        elif username == '' :
            result['message'] = '이름을 입력해주세요.'
            return JsonResponse(result, status=202)
        elif nickname == '' :
            result['message'] = '닉네임을 입력해주세요.'
            return JsonResponse(result, status=202)
        elif gender == None :
            result['message'] = '성별을 선택해주세요.'
            return JsonResponse(result, status=202)
        
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

def log_in(request):
    if request.method == 'POST' :
        data = json.loads(request.body)
        email = data['email']
        password = data['password']
        user = authenticate(email=email, password=password)
        if user:
            auth.login(request, user)
            return redirect('rcmd:service')
        else:
            result = {'response': "error"}
            return JsonResponse(result, status=200)


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
            
              