from bs4 import BeautifulSoup
import requests
import re
from .models import Artwork

def crawl_naverwebtoon():
    naver_webtoon_urls = ["https://comic.naver.com/webtoon/weekday","https://comic.naver.com/webtoon/finish"]#연재 완결
    webtoons_url = []
    for naver_webtoon_url in naver_webtoon_urls:
        res = requests.get(naver_webtoon_url)
        soup = BeautifulSoup(res.content, "html.parser")
        if naver_webtoon_url == naver_webtoon_urls[0]:
            webtoons_url.extend(soup.find('div', class_ = 'list_area daily_all').find_all("li"))
        if naver_webtoon_url == naver_webtoon_urls[1]:
            webtoons_url.extend(soup.find('div', class_ = 'list_area').find_all("li"))
            
    base_path = 'http://comic.naver.com'
    webtoon_info_list = []
    for webtoon_url in webtoons_url:
        webtoon_info_dic = {}
        detail_webtoon_url = base_path+webtoon_url.select_one('a').attrs['href']
        if detail_webtoon_url == '#':
            continue    
        response_webtoon_detail = requests.get(detail_webtoon_url)
        soup_detail = BeautifulSoup(response_webtoon_detail.content, "html.parser")
        uid = re.sub("[^0-9]","",detail_webtoon_url.split('titleId=')[1][:7])
        title = soup_detail.select_one('span.title').text
        story = soup_detail.select_one('p').text
        webtoon_info_dic['uid'] = uid
        webtoon_info_dic['title'] = title
        webtoon_info_dic['url'] = detail_webtoon_url
        webtoon_info_dic['story'] = story
        webtoon_info_dic['enable'] = False
        webtoon_info_list.append(Artwork(**webtoon_info_dic))
    return webtoon_info_list