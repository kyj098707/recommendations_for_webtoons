from django.shortcuts import render
from .models import Detail


def home(request):
    data = Detail.objects.all()
    print(data)
    return render(request, "recommendationapp/base.html")