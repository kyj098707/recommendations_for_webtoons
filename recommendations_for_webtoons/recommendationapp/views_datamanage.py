from .models import *
import requests

##todo 본 DB 접속 url도 settings.py 내 key처럼 로컬 conf로 별도로 빼 둘 것.

def clear_db():
	Rel_ar_aw.objects.all().delete()
	Rel_gr_aw.objects.all().delete()
	Sim_st_st.objects.all().delete()
	Sim_th_th.objects.all().delete()
	Artist.objects.all().delete()
	Artwork.objects.all().delete()
	Publisher.objects.all().delete()
	Genre.objects.all().delete()
	
def write_pub():
	s = Publisher(name="Naver")
	s.save()
	s = Publisher(name="Daum/KAKAO")
	s.save()
	
def write_baseinfo():
	response = requests.get('http://kt-aivle.iptime.org:64000/test/get_base')
	artists = response.json()['artist']
	bulk = []
	for i in artists:
		dict = {'name': i}
		bulk.append(Artist(**dict))
	Artist.objects.bulk_create(bulk)
	
	genres = response.json()['genre']
	bulk = []
	for i in genres:
		dict = {'name': i.strip()}
		bulk.append(Genre(**dict))
	Genre.objects.bulk_create(bulk)

def write_artwork(Pub):
	response = requests.get('http://kt-aivle.iptime.org:64000/test/get_artwork')
	response = response.json()['response']
	bulk = []
	for i in response:
		dict = {}
		dict['token'] = i['token']
		dict['uid'] = i['uid']
		dict['title'] = i['title']
		dict['publisher'] = Pub[i['publisher_name']]
		dict['story'] = i['story']
		dict['url'] = i['url']
		dict['thumbnail_url'] = i['thumbnail_url']
		if i['rating'] <= 5:
			dict['rating'] = 9 + i['rating'] / 10
		else:
			dict['rating'] = i['rating']
		bulk.append(Artwork(**dict))
	Artwork.objects.bulk_create(bulk)

def write_rel(gl, al, wl):
	response = requests.get('http://kt-aivle.iptime.org:64000/test/get_artist')
	response = response.json()['response']
	bulk = []
	for i in response:
		for j in response[i]:
			token, uid = j
			artist, type = i.split("%%")
			dict = {}
			dict['r_artist'] = al[artist]
			dict['r_artwork'] = wl[token + "%%%" + str(uid)]
			dict['type'] = type
			bulk.append(Rel_ar_aw(**dict))
	Rel_ar_aw.objects.bulk_create(bulk)
	
	response = requests.get('http://kt-aivle.iptime.org:64000/test/get_genre')
	response = response.json()['response']
	bulk = []
	for i in response:
		dict = {}
		dict['r_genre'] = gl[i['name']]
		token, uid = i['Artwork__token'], i['Artwork__uid']
		dict['r_artwork'] = wl[token + "%%%" + str(uid)]
		bulk.append(Rel_gr_aw(**dict))
	Rel_gr_aw.objects.bulk_create(bulk)
	
def write_thumbs_rel():
	response = requests.get('http://kt-aivle.iptime.org:64000/test/get_thumbs')
	response = response.json()
	print(response)
	alls = {str(i.token)+"_"+str(i.uid) : i for i in Artwork.objects.all()}
	bulk = []
	for i in response:
		for j in response[i]:
			token, uid = i.split("_")
			value, target = j
			token2, uid2 = target.split("_")
			dict = {}
			dict['r_artwork1'] = alls[i]
			dict['r_artwork2'] = alls[target]
			dict['similarity'] = value
			bulk.append(Sim_th_th(**dict))
	Sim_th_th.objects.bulk_create(bulk)
	

def write_storys_rel():
	response = requests.get('http://kt-aivle.iptime.org:64000/test/get_storys')
	response = response.json()
	print(response)
	alls = {str(i.token)+"_"+str(i.uid) : i for i in Artwork.objects.all()}
	bulk = []
	for i in response:
		for j in response[i]:
			token, uid = i.split("_")
			value, target = j
			token2, uid2 = target.split("_")
			dict = {}
			dict['r_artwork1'] = alls[i]
			dict['r_artwork2'] = alls[target]
			dict['similarity'] = value
			bulk.append(Sim_st_st(**dict))
	Sim_st_st.objects.bulk_create(bulk)