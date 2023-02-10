import json
from django.shortcuts import render
from .parser import *
from .models import *
from .views_datamanage import *
from django.db import transaction
from collections import Counter
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404

@csrf_exempt
def manage_data(request):
    # http://127.0.0.1:8000/manage_data
    # 본 페이지 들어가시면 DB 제어할 수 있는 버튼 뜹니다.
    # 한번 누르고 기다리면 진행되며, alert 팝업으로 완료 여부가 출력됩니다.
    
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
    return render(request, "./__manage/data.html", {}) # app 내의 templete 폴더 참조



def testpage(request):  
    # http://localhost:8000/testpage

    data = {'pack' : []}
    return render(request, "./testpage/sample.html", data)


def testpage2(request):
    # http://localhost:8000/testpage2
    with transaction.atomic():
        sim_bulk_crt = find_story_similarity()
        Sim_st_st.objects.bulk_create(sim_bulk_crt)
        
    data = {'pack' : {'':''}} # front로 데이터를 던지기 위해 pack (body.html 참조)
    return render(request, "./testpage/sample.html", data) # app 내의 templete 폴더 참조
#---------------------------------------------------------------------------------------#


def selection(request):
    # conn = pymongo.MongoClient("mongodb://172.30.1.15:27017/?authMechanism=DEFAULT&authSource=webtoon_db")
    # webtoon_db = conn.webtoon_db
    # webtoon_collection = webtoon_db.webtoon_collection
    # if request.POST:
    #     webtoon_title = request.POST['webtoon_title']
    #
    #     similarity = webtoon_collection.find_one({'title':webtoon_title},{'_id':0,'similarity':1})['similarity']
    #     return render(request, "recommendationapp/base.html",{"similarity":similarity,'post':True})
    return render(request, "__main/service_page.html")

def recommendation(request):
    return render(request, "recommendationapp/recommendation.html")


def select(request):
    return render(request,'recommendationapp/select.html')


def results(request):
    input_title_list = ['퀘스트지상주의','김부장','싸움독학','존망코인' , '신림/남/22']
    genre_list = []
    artist_list = []
    for input_title in input_title_list:
        genre_model_data = Rel_gr_aw.objects.filter(r_artwork__title=input_title)
        artist_model_data = Rel_ar_aw.objects.filter(r_artwork__title=input_title)
        for g,a in zip(genre_model_data,artist_model_data):
            genre_list.append(g.r_genre.name)
            artist_list.append(a.r_artist.name)
            
    most_genre = Counter(genre_list).most_common() # 장르 3개 정도 보여주기
    most_artist = Counter(artist_list).most_common()[0][0]
    for i in range(3):
        print(f"많이 나온 장르 {most_genre[i][0]}입니다. 이런 {most_genre[i][0]}작품들은 어떠세요?!")
        genre_data = Rel_gr_aw.objects.filter(r_genre__name=most_genre[0][0])[:10]
        for g in genre_data:
            print(f"{most_genre[i][0]} : {g.r_artwork.title}")


    print(f"가장 많이 나온 작가는 {most_artist}입니다. 다른 {most_artist}님의 작품들은 어떠세요?!") # 다른 작품이 있을 때만 뜨는 걸로
    artist_data = Rel_ar_aw.objects.filter(r_artist__name=most_artist)[:10]
    for g in artist_data:
        if g.r_artwork.title in input_title_list:
            continue
        print(f"{most_artist} : {g.r_artwork.title}")
    
    for input_title in input_title_list:
        print(f" << {input_title} >> 작품을 좋아하셨나요? 이 작품들은 어떤가요?")
        r_artwork1 = Artwork.objects.get(title=input_title)
        story_sim_data =Sim_st_st.objects.filter(r_artwork1=r_artwork1)
        for data in story_sim_data[:10]:
            print( "연관된 작품들: ", data.r_artwork2.title )
    


    return render(request,'recommendationapp/results.html')
