from django.shortcuts import render

def intro(request):
    return render(request, "./_01_intro/main.html")

def about(request):
    return render(request, "./base.html")