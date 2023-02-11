import json
from django.shortcuts import render
from .parser import *
from .models import *
from .views_datamanage import *
from django.db import transaction
from collections import Counter
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404
from django.template.loader import render_to_string

def service_test(request):
    # http://localhost:8000/service_test
    data1 = Genre.objects.all()
    data = {'data1': data1}
    return render(request, "./_02_service/main.html", data)