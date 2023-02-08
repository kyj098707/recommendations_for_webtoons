from bs4 import BeautifulSoup
import requests

def crawl_naverwebtoon():
    naver_webtoon_url = "https://comic.naver.com/webtoon/weekday"
    res = requests.get(naver_webtoon_url)
    soup = BeautifulSoup(res.content, "html.parser")
    webtoons_url = soup.find('div', class_ = 'list_area daily_all').find_all("li")
    base_path = 'http://comic.naver.com'
    webtoon_info_list = []
    for webtoon_url in webtoons_url:
        webtoon_info_dic = {}
        detail_webtoon_url = base_path+webtoon_url.select_one('a').attrs['href']
        response_webtoon_detail = requests.get(detail_webtoon_url)
        soup_detail = BeautifulSoup(response_webtoon_detail.content, "html.parser")
        title = soup_detail.select_one('span.title').text
        story = soup_detail.select_one('p').text
        webtoon_info_dic['title'] = title
        webtoon_info_dic['url'] = detail_webtoon_url
        webtoon_info_dic['story'] = story
        webtoon_info_list.append(webtoon_info_dic)
    return webtoon_info_list