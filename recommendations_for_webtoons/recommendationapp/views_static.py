from django.shortcuts import render

def intro(request):
    user = request.user
    data = {'user_status' : user.is_authenticated}
    return render(request, "./_01_intro/main.html", data)

def about(request):
    user = request.user
    data = {'user_status' : user.is_authenticated}
    return render(request, "./base.html", data)