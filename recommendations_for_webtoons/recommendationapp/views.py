# from .parser import
import json
from django.shortcuts import render
from .models import *
from .views_datamanage import *
from django.db import transaction
from collections import Counter
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404
from django.template.loader import render_to_string
from .parser import *


@csrf_exempt
def manage_data(request):
    # http://127.0.0.1:8000/manage_data
    # 본 페이지 들어가시면 DB 제어할 수 있는 버튼 뜹니다.
    # 한번 누르고 기다리면 진행되며, alert 팝업으로 완료 여부가 출력됩니다.
    
    # 본 서버 데이터 內 작품 약 3700개. 작가 4k명 이상 집계.
    
    indicator = request.POST.get('indicator')
    if indicator == "delete_all_data":
        clear_db()
        result = {'response': 'complete'}
        return HttpResponse(json.dumps(result), content_type="application/json")

    elif indicator == "download_all_data":
        write_pub()
        write_baseinfo()
        Pub = {i.name : i for i in Publisher.objects.all()}
        write_artwork(Pub)
        gl = {i.name : i for i in Genre.objects.all()}
        al = {i.name : i for i in Artist.objects.all()}
        wl = {i.token+"%%%"+str(i.uid) : i for i in Artwork.objects.all()}
        write_rel(gl, al, wl)
        result = {'response': 'complete'}
        return HttpResponse(json.dumps(result), content_type="application/json")
    
    elif indicator == "read_genre":
        model = Genre.objects.all()
        html = render_to_string('./__manage/__genre_table.html', {'data': model})
        result = {'response': 'complete', 'html':html}
        return HttpResponse(json.dumps(result), content_type="application/json")
    
    return render(request, "./__manage/data.html", {}) # app 내의 templete 폴더 참조


def testpage(request):
    # http://localhost:8000/testpage
    with transaction.atomic():
        sim_bulk_crt = find_story_similarity()
        Sim_st_st.objects.bulk_create(sim_bulk_crt)
        
    data = {'pack' : {'':''}} # front로 데이터를 던지기 위해 pack (body.html 참조)
    return render(request, "./__test/__learn.html", data) # app 내의 templete 폴더 참조