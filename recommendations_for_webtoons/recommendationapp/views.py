from django.shortcuts import render
# import pymongo
from .models import *
from django.db import transaction

def testpage(request):
    # http://localhost:8000/recommendation/testpage

    # uid unique 해제했습니다.
    if Artwork.objects.all().count() < 50 : # 결과가 50개 이하면, 생성을 하지 않겠습니다.
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
    
    model_data = Artwork.objects.all()[:30] # 전체 모델 중 30개만 불러오겠습니다.
    
    print(model_data) # 콘솔에, 불러온 데이터의 상황이 출력됩니다. (객체로)

    for i in model_data: # 또는 이와 같이 콘솔에서 확인 가능합니다.
        print("불러온 타이틀은", i.title, "입니다.")
        
    data = {'pack' : model_data} # front로 데이터를 던지기 위해 pack (body.html 참조하세요)
    return render(request, "./testpage/sample.html", data) # app 내의 templete 폴더 참조


def home(request):
    # conn = pymongo.MongoClient("mongodb://172.30.1.15:27017/?authMechanism=DEFAULT&authSource=webtoon_db")
    # webtoon_db = conn.webtoon_db
    # webtoon_collection = webtoon_db.webtoon_collection
    # if request.POST:
    #     webtoon_title = request.POST['webtoon_title']
    #
    #     similarity = webtoon_collection.find_one({'title':webtoon_title},{'_id':0,'similarity':1})['similarity']
    #     return render(request, "recommendationapp/base.html",{"similarity":similarity,'post':True})
    return render(request, "recommendationapp/base.html")



