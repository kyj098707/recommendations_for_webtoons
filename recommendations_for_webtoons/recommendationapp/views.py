from django.shortcuts import render
from .parser import crawl_naverwebtoon
from .models import *
from django.db import transaction

"""def testpage(request):  
    # http://localhost:8000/testpage

    # 생성 및 트랜잭션 Example.
    # uid unique 해제했습니다.
    if Artwork.objects.all().count() < 50 : # 현재 Artwork내 data가 50개 이상이면, 생성을 하지 않겠습니다.
        with transaction.atomic(): # 다중 쿼리 실행에서, 하나라도 실패한다면 롤백. (with문 내에서)
            webtoon_bulk_crt,writer_bulk_crt,genre_type_list = crawl_naverwebtoon()
            Artwork.objects.bulk_create(webtoon_bulk_crt)
            Rel_ar_aw.objects.bulk_create(writer_bulk_crt)
            Rel_gr_aw.objects.bulk_create(genre_type_list)
    # 즉, 연산 도중에 DB에 값을 쓰면서 내려가다가 뻗으면 더미 데이터가 남지만,
    # 이 방식을 쓰면 괜찮습니다.
    
    # 유무 확인 및 검색 Example
    ###count나 exists 모두 유무를 파악하지만, exists가 성능이 좋습니다. ###
    
    model_data = Artwork.objects.all()[:30] # 전체 모델 중 30개만 불러오겠습니다.

    # 콘솔 출력 Example
    print(model_data) # 콘솔에, 불러온 데이터의 상황이 출력됩니다. (객체로)
    for i in model_data: # 또는 이와 같이 콘솔에서 확인 가능합니다.
        print("불러온 타이틀은", i.title, "입니다.")

    # 사용자 출력 Example
    data = {'pack' : model_data} # front로 데이터를 던지기 위해 pack (body.html 참조)
    return render(request, "./testpage/sample.html", data) # app 내의 templete 폴더 참조


def testpage2(request):
    # http://localhost:8000/testpage2
    model_data = Rel_ar_aw.objects.filter(r_artist__name="박태준 만화회사", type='Author')
    # r_artist가 가리키는 Artist 테이블 내 이름을 검색
    for i in model_data :
        print("박태준 만화회사가 글 작가가 참여한 작품 타이틀은", i.r_artwork.title)

    
    data = {'pack2': model_data}  # front로 데이터를 던지기 위해 pack2로 (body.html 참조)
    return render(request, "./testpage/sample.html", data)  # app 내의 templete 폴더 참조
"""

def recommendation(request):
    return render(request, "recommendationapp/recommendation.html")


def select(request):
    return render(request,'recommendationapp/select.html')


def results(request):
    return render(request,'recommendationapp/results.html')
