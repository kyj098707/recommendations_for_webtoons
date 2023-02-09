from bs4 import BeautifulSoup
import requests
import re
from .models import *

def crawl_naverwebtoon():
    days = ['mon','tue','wed','thu','fri','sat','sun']
    
    naver_webtoon_urls = [f"https://comic.naver.com/webtoon/weekdayList?week={day}" for day in days] + ["https://comic.naver.com/webtoon/finish"]#요일별 +  완결
    webtoons_url = []
    for naver_webtoon_url in naver_webtoon_urls:
        res = requests.get(naver_webtoon_url)
        soup = BeautifulSoup(res.content, "html.parser")
        if naver_webtoon_url == naver_webtoon_urls[-1]:
            webtoons_url.extend(soup.find('div', class_ = 'list_area').find_all("li"))
        else:
            webtoons_url.extend(soup.find('div', class_ = 'list_area daily_img').find_all("li"))

    base_path = 'http://comic.naver.com'
    webtoon_info_list = []
    writer_info_list =[]
    genre_types_list = []
    for webtoon_url in webtoons_url:
        writer_info = {}
        webtoon_info_dic = {}
        star = webtoon_url.select_one('strong').text
        detail_webtoon_url = base_path+webtoon_url.select_one('a').attrs['href']
        response_webtoon_detail = requests.get(detail_webtoon_url)
        soup_detail = BeautifulSoup(response_webtoon_detail.content, "html.parser")
        uid = re.sub("[^0-9]","",detail_webtoon_url.split('titleId=')[1][:7])
        title = soup_detail.select_one('span.title').text
        story = soup_detail.select_one('p').text
        writers = list(map(lambda x :x.lstrip(),soup_detail.select_one('span.wrt_nm').text.split(' / ')))        
        genre_types = list(map(lambda x :x.lstrip(),soup_detail.select_one('span.genre').text.split(',')))        
        
        if len(writers) == 1:
            writer_info['Author'] = writer_info['Illust'] = writers[0]
        elif len(writers) == 2:
            writer_info['Author'],writer_info['Illust'] = writers
        else:
            writer_info['Author'],writer_info['Illust'],writer_info['Origin'] = writers
        webtoon_info_dic['uid'] = "N_"+uid
        webtoon_info_dic['title'] = title
        webtoon_info_dic['url'] = detail_webtoon_url
        webtoon_info_dic['story'] = story
        webtoon_info_dic['enable'] = False
        webtoon_info_dic['star'] = float(star)
        artwork = Artwork(**webtoon_info_dic)
        for k,v in writer_info.items():
            artist = ''
            if not Artist.objects.filter(name=v).exists():
                artist = Artist(name=v)
                artist.save()
            artist = Artist.objects.get(name=v)
            res = Rel_ar_aw(r_artist=artist,r_artwork=artwork, type=k)
            writer_info_list.append(res)
        webtoon_info_list.append(artwork)
        for gen in genre_types:
            genre = ''
            if not Genre.objects.filter(name=gen).exists():
                genre = Genre(name=gen)
                genre.save()
            genre = Genre.objects.get(name=gen)
            res = Rel_gr_aw(r_genre=genre,r_artwork=artwork)
            genre_types_list.append(res)
    return webtoon_info_list,writer_info_list,genre_types_list