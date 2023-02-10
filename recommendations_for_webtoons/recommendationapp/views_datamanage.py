from .models import *
import requests

def clear_db():
	Rel_ar_aw.objects.all().delete()
	Rel_gr_aw.objects.all().delete()
	Sim_st_st.objects.all().delete()
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