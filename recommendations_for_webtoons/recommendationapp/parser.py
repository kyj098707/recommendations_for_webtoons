from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer, util
from transformers import ViTForImageClassification
import requests
import re
from .models import *
from glob import glob
import albumentations as A
from albumentations.pytorch.transforms import ToTensorV2
import torch
from .util.models import *
from .util.dataset import *

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
    uid_check = {}
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
        if uid_check.get(uid):
            continue
        uid_check[uid] = 1
        title = soup_detail.select_one('span.title').text
        story = soup_detail.select_one('p').text
        path_thumb = soup_detail.select_one('img').attrs['src']
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
        webtoon_info_dic['path_thumb'] = path_thumb
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

def find_sim(story1, story2, checkpoints):
    story_vector1 = checkpoints.encode(story1)
    story_vector2 = checkpoints.encode(story2)
    story_sims = util.cos_sim(story_vector1,story_vector2)
    return story_sims

def find_story_similarity():
    base_uid_list = [b.uid for b in Artwork.objects.all()]
    base_story_list = [re.sub("[^ 0-9가-힣A-Za-z]",'',b.story) for b in Artwork.objects.all()]
    
    compare_uid_list = [c.uid for c in Artwork.objects.all()]
    compare_story_list = [re.sub("[^ 0-9가-힣A-Za-z]",'',c.story) for c in Artwork.objects.all()]
    checkpoints = SentenceTransformer('snunlp/KR-SBERT-V40K-klueNLI-augSTS')
    
    sim_list = find_sim(base_story_list,compare_story_list,checkpoints)
    sim_story_list = []
    for idx,uid in enumerate(base_uid_list):
        sims = [(sim,t) for sim,t in zip(sim_list[idx],compare_uid_list)]
        sims = sorted(sims,reverse=True)[:20]
        
        base_artwork = Artwork.objects.get(uid=sims[0][1])
        
        for sim in sims[1:]:
            compare_artwork = Artwork.objects.get(uid=sim[1])
            res = Sim_st_st(r_artwork1=base_artwork,r_artwork2=compare_artwork,similarity=sim[0].item())
            sim_story_list.append(res)

    return sim_story_list

def infer(model, test_loader, device):
    model.to(device)
    model.eval()
    predictions = []
    with torch.no_grad():
        for imgs in test_loader:
            imgs = imgs.float().to(device)
            
            probs = model(imgs)
            probs  = probs.cpu().detach().numpy()
            preds = probs.astype(float)
            predictions += preds.tolist() 
    return predictions

def find_thumbnail_similarity():
    test_transform = A.Compose([A.Resize(480, 480),
                                A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225), max_pixel_value=255.0, always_apply=False, p=1.0),
                                ToTensorV2()])
    
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    base_uid_list = [b.uid for b in Artwork.objects.all()]
    compare_uid_list = [c.uid for c in Artwork.objects.all()]
    
    model = torch.load("./comic_165label.pth")
    newmodel = EfficientV2Backbone(model)
    
    th_similarity_list = []
    sim_th_list = []
    for base_uid in base_uid_list:
        for compare_uid in compare_uid_list:
            if base_uid == compare_uid:
                continue
            img1 = sorted(glob(f"./data/{base_uid}/*.jpg"))[1:]
            img2 = sorted(glob(f"./data/{compare_uid}/*.jpg"))[1:]
            test_dataset1 = WebtoonDataset(img1, None, test_transform)
            test_loader1 = DataLoader(test_dataset1, batch_size = 16, shuffle=False)
            test_dataset2 = WebtoonDataset(img2, None, test_transform)
            test_loader2 = DataLoader(test_dataset2, batch_size = 16, shuffle=False)
            preds1 = infer(newmodel, test_loader1, device)
            preds2 = infer(newmodel, test_loader2, device)

            sim = util.cos_sim(preds1,preds2)
            mean_similarity = sim.numpy().mean()

            th_similarity_list.append((mean_similarity,compare_uid))
        th_similarity_list = sorted(th_similarity_list, reverse=True)[:20]
        
        base_artwork = Artwork.get(uid=base_uid)
        for sim in th_similarity_list:
            compare_artwork = Artwork.objects.get(uid=sim[1])
            res = Sim_th_th(r_artwork1=base_artwork,r_artwork2=compare_artwork,similarity=mean_similarity)
            sim_th_list.append(res)
    return sim_th_list