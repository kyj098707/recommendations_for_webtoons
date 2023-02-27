import json
from django.shortcuts import render
from .models import *
from .views_datamanage import *
from django.db import transaction
from collections import Counter
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404
from django.template.loader import render_to_string

def service_test(request):
    # http://localhost:8000/service_test
    indicator = request.POST.get('indicator')
    
    if indicator == "get_startswith":
        keyword = request.POST.get('keyword')
        print(keyword)
        data = Artwork.objects.filter(title__startswith=keyword)[0:15]
        html = render_to_string('_02_service\\__addon\\startswith_list.html', {'data': data})
        return HttpResponse(html)

    elif indicator == "get_aw_detail":
        keyword = request.POST.get('keyword')
        token, uid = keyword.split("_")
        data = Artwork.objects.get(token=token, uid = uid)
        html = render_to_string('_02_service\\__addon\\modal_detail_artwork.html', {'data': data})
        return HttpResponse(html)


    user = request.user
    data1 = Genre.objects.all()
    data = {'data1': data1, 'user_status' : user.is_authenticated}
    return render(request, "./_02_service/main.html", data)