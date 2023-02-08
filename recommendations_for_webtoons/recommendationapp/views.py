from django.shortcuts import render
# import pymongo
from .models import *
from django.db import transaction

def testpage(request):
    # http://localhost:8000/recommendation/testpage

    # 생성 및 트랜잭션 Example.
    # uid unique 해제했습니다.
    if Artwork.objects.all().count() > 50 : # 현재 Artwork내 data가 50개 이상이면, 생성을 하지 않겠습니다.
        with transaction.atomic(): # 다중 쿼리 실행에서, 하나라도 실패한다면 롤백. (with문 내에서)
            bulk_crt = []  # 빈 배열
            for i in range(1, 95): # 임의의 Artwork 값 생성
                dict = {'uid' : int(i)*i,
                        'title' : f'타이틀{str(i).zfill(9)}',
                        'story' : f'{str(i)*i}',
                        'enable' : False}
                # 즉, json 파일을 받아 key만 바꿔 바로 던질 수 있습니다.
                bulk_crt.append(Artwork(**dict))
                # dictionary unpacking : **
            Artwork.objects.bulk_create(bulk_crt)
            # 대용량 생성
    # 즉, 연산 도중에 DB에 값을 쓰면서 내려가다가 뻗으면 더미 데이터가 남지만,
    # 이 방식을 쓰면 괜찮습니다.
    
    # 유무 확인 및 검색 Example
    ###count나 exists 모두 유무를 파악하지만, exists가 성능이 좋습니다. ###
    if Artwork.objects.filter(title="용사").count() : #Artwork 내 "용사" 타이틀을 가진 작품이 5개 이상이면,
        print("용사가 많이 있다.") # 콘솔에 용사가 나타났다.를 출력합니다.
    elif Artwork.objects.filter(title__startswith="용사").exists() : #Artwork 내 "용사"로 시작하는 작품이 존재하면,
        print("용사로 시작하는 친구가 존재하긴 한다.")
    
    model_data = Artwork.objects.all()[:30] # 전체 모델 중 30개만 불러오겠습니다.

    # 콘솔 출력 Example
    print(model_data) # 콘솔에, 불러온 데이터의 상황이 출력됩니다. (객체로)
    for i in model_data: # 또는 이와 같이 콘솔에서 확인 가능합니다.
        print("불러온 타이틀은", i.title, "입니다.")

    # 사용자 출력 Example
    data = {'pack' : model_data} # front로 데이터를 던지기 위해 pack (body.html 참조하세요)
    return render(request, "./testpage/sample.html", data) # app 내의 templete 폴더 참조


def selection(request):
    # conn = pymongo.MongoClient("mongodb://172.30.1.15:27017/?authMechanism=DEFAULT&authSource=webtoon_db")
    # webtoon_db = conn.webtoon_db
    # webtoon_collection = webtoon_db.webtoon_collection
    # if request.POST:
    #     webtoon_title = request.POST['webtoon_title']
    #
    #     similarity = webtoon_collection.find_one({'title':webtoon_title},{'_id':0,'similarity':1})['similarity']
    #     return render(request, "recommendationapp/base.html",{"similarity":similarity,'post':True})
    return render(request, "recommendationapp/selection.html")

def recommendation(request):
    # conn = pymongo.MongoClient("mongodb://172.30.1.15:27017/?authMechanism=DEFAULT&authSource=webtoon_db")
    # webtoon_db = conn.webtoon_db
    # webtoon_collection = webtoon_db.webtoon_collection
    # if request.POST:
    #     webtoon_title = request.POST['webtoon_title']
    #
    #     similarity = webtoon_collection.find_one({'title':webtoon_title},{'_id':0,'similarity':1})['similarity']
    #     return render(request, "recommendationapp/base.html",{"similarity":similarity,'post':True})
    return render(request, "recommendationapp/recommendation.html")


