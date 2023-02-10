from django.shortcuts import render
from .parser import *
from .models import *
from django.db import transaction
from collections import Counter 

def testpage(request):  
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
    with transaction.atomic():
        sim_bulk_crt = find_story_similarity()
        Sim_st_st.objects.bulk_create(sim_bulk_crt)
#---------------------------------------------------------------------------------------#



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
