import requests
from bs4 import BeautifulSoup
import re
import os

def save_img(url,dir_path):
    img = requests.get(url).content
    file = open(dir_path,"wb")
    file.write(img)
    file.close()

def crawl_naverwebtoon_img():

    # 요일, 완결 웹툰 url을 저장
    days = ['mon','tue','wed','thu','fri','sat','sun']
    naver_webtoon_urls = [f"https://comic.naver.com/webtoon/weekdayList?week={day}" for day in days] + ["https://comic.naver.com/webtoon/finish"]#요일별 +  완결
    
    # 요일, 완결 웹툰 url로 들어가서 webtoons_url에 각 웹툰의 덩어리들을 저장
    webtoons_url = []
    for naver_webtoon_url in naver_webtoon_urls:
        res = requests.get(naver_webtoon_url)
        soup = BeautifulSoup(res.content, "html.parser")
        if naver_webtoon_url == naver_webtoon_urls[-1]:
            webtoons_url.extend(soup.find('div', class_ = 'list_area').find_all("li"))
        else:
            webtoons_url.extend(soup.find('div', class_ = 'list_area daily_img').find_all("li"))
    
    # 월, 수 웹툰등으로 겹치는 웹툰 체크
    uid_check = {}

    # 웹툰 덩어리에서 웹툰의 title_id를 가져오기
    base_path = 'http://comic.naver.com'
    for webtoon_url in webtoons_url:
        detail_webtoon_url = base_path+webtoon_url.select_one('a').attrs['href']
        response_webtoon_detail = requests.get(detail_webtoon_url)
        soup = BeautifulSoup(response_webtoon_detail.content, 'html.parser')
        # 겹치는 웹툰 체크
        uid = re.sub("[^0-9]","",detail_webtoon_url.split('titleId=')[1][:7])
        if uid_check.get(uid):
            continue
        uid_check[uid] = 1
        os.makedirs(f'./data/N_{uid}',exist_ok=True)
        data_path = f"./data/N_{uid}/{0}.jpg"
        thumb = soup.select_one('img').attrs['src']
        save_img(thumb,data_path)
        # 같은 웹툰 안에 여러 페이지가 존재
        page = 1
        cnt = 1
        
        while True:
            url = f"{detail_webtoon_url}&page={page}"
            res = requests.get(url)
            soup = BeautifulSoup(res.text, 'html.parser')
            viewList = soup.select('.viewList tr')
            for view in viewList[3:]: # 배너 제외
                imgSrc = view.select_one('a > img').attrs.get('src')
                data_path = f"./data/N_{uid}/{cnt}.jpg"
                save_img(imgSrc,data_path)
                cnt += 1
            if soup.select_one('a.next') == None:
                break
            page += 1


if __name__ == "__main__":
    crawl_naverwebtoon_img()