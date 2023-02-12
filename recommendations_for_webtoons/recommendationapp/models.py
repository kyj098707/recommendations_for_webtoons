from django.db import models

# Create your models here.

# HeidiSQL 통해서
# db_info.conf 문서 참조하여 로그인하시면 생성된 DB를 볼 수 있습니다.

class Detail(models.Model):
    title_id = models.CharField(max_length=15, blank=True, null=True)
    title = models.CharField(max_length=20, blank=True, null=True)
    website = models.CharField(max_length=10, blank=True, null=True)
    story = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detail'

class Artist(models.Model):
    name = models.CharField(max_length=255, default='', null=True, blank=True)

class Genre(models.Model):
    name = models.CharField(max_length=255, default='', null=True, blank= False)# 장르 이름에 blank 없앴습니다!
    count = models.IntegerField(default=0, blank=True, null=True)
    
    def disp_artwork(self):
        print(self.name)
        print(Rel_gr_aw.objects.filter(r_genre__name=self.name).count())
        return Rel_gr_aw.objects.filter(r_genre__name=self.name)[1:13]

class Publisher(models.Model):
    name = models.CharField(max_length=255, default='', null=True, blank=True)
    count = models.IntegerField(default=0, blank=True, null=True)

class Artwork(models.Model): # DB Table 첫글자 대문자로 맞추겠습니다. 이하 컬럼 소문자.
    token = models.CharField(max_length=1, default='')
    uid = models.IntegerField(default='0')
    title = models.CharField(max_length=255, default='', null=True, blank=True)
    #    외래키
    # on_delete = models.PROTECT : 장르가 지워질 때, 장르 아래 Artwork가 존재하면 지워지지 않게 함.
    publisher = models.ForeignKey(Publisher, on_delete = models.PROTECT, related_name='publish', blank=True, null=True)

    rating = models.FloatField(default=0, null=True, blank=True) # 평점
    
    # story, url => 255자 이상 길 수 있으므로 textfield 지정
    story = models.TextField(default='', null=True, blank=True)
    url = models.TextField(default='', null=True, blank=True)
    thumbnail_url = models.TextField(default='', null=True, blank=True)
    
    # 일반 os에서 경로 255자 제한이므로, 다중 행을 다룰 이유 또한 없으므로.
    path_thumb = models.CharField(max_length=255, default='', null=True, blank=True)
    
    # 참 거짓 필드
    enable = models.BooleanField(default=True)

    class Meta:
        ordering = ['title'] # 기본적으로 db에서 불러올 때 title 순으로 정렬
        unique_together = ['token', 'uid']
        
    def temp_thumbpath(self):
        return f'http://kt-aivle.iptime.org:64000/static/mainsource/thumb/{self.token}_{self.uid}.jpg'


#============================================================================
#============================================================================
# 다대다 필드 구현 : manytomanyField 사용치 않고 직접 구현하겠습니다.
# Through model을 포함하여 직접 정의합니다.

class Rel_ar_aw(models.Model): #N개의 작가들이 N개의 작품에 대해 붙을 수 있으므로, 다대다 관계
    r_artist = models.ForeignKey(Artist, on_delete = models.PROTECT, related_name='ar_aw', blank=True, null=True)
    r_artwork = models.ForeignKey(Artwork, on_delete = models.PROTECT, related_name='aw_ar', blank=True, null=True)
    type = models.CharField(max_length=255, default='', null=True, blank=True)
    # 해당 작가-작품이 어떤 관계인지(글작가, 그림작가, 원작자, 배급사) 타입 기재
    
    class Meta:
        ordering = ['r_artist__name', 'r_artwork__title', 'type']
        # 일반적으로 산출할 때, 한 작가의 같은 작품을 우선하여 type 순으로 가져옵니다.


class Rel_gr_aw(models.Model): # 장르 - 작품 다대다 관계필드
    # 장르 또한 다중장르 작업을 진행하기로 하였으므로. 위와 동일
    r_genre = models.ForeignKey(Genre, on_delete = models.PROTECT, related_name='gr_aw', blank=True, null=True)
    r_artwork = models.ForeignKey(Artwork, on_delete = models.PROTECT, related_name='aw_gr', blank=True, null=True)

    class Meta:
        ordering = ['r_artwork__title']
        # 일반적으로 산출할 때, 숫자순/알파벳순/가나다순으로 가져옵니다.

class Sim_st_st(models.Model): #story 유사도
    r_artwork1 = models.ForeignKey(Artwork, on_delete = models.PROTECT, related_name='st1_st2' ,blank=True, null=True)
    r_artwork2 = models.ForeignKey(Artwork, on_delete = models.PROTECT,related_name='st2_st1',blank=True, null=True)
    similarity = models.FloatField(default=0, null=True, blank=False)   

    class Meta:
        ordering = ['similarity']
#============================================================================
#============================================================================
