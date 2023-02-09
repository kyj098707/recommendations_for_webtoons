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
        
        
class Genre(models.Model):
    name = models.CharField(max_length=255, default='', null=True, blank=True)
    count = models.IntegerField(default=0, blank=True, null=True)


class Publisher(models.Model):
    name = models.CharField(max_length=255, default='', null=True, blank=True)
    count = models.IntegerField(default=0, blank=True, null=True)


class Artwork(models.Model): # DB Table 첫글자 대문자로 맞추겠습니다. 이하 컬럼 소문자.
    uid = models.CharField(max_length=20, default='', null=True, blank=True) # 폐기예정
    star = models.FloatField(default=0,null=True,blank=True) # 평점
    title = models.CharField(max_length=255, default='', null=True, blank=True)
    artist = models.CharField(max_length=100, default='', null=True, blank=True)
    # 외래키
    # on_delete = models.PROTECT : 장르가 지워질 때, 장르 아래 Artwork가 존재하면 지워지지 않게 함.
    genre = models.ForeignKey(Genre, on_delete = models.PROTECT, related_name='genre', blank=True, null=True)
    publisher = models.ForeignKey(Publisher, on_delete = models.PROTECT, related_name='publish', blank=True, null=True)
    
    # story, url => 255자 이상 길 수 있으므로 textfield 지정
    story = models.TextField(default='', null=True, blank=True)
    url = models.TextField(default='', null=True, blank=True)
    
    # 일반 os에서 경로 255자 제한이므로, 다중 행을 다룰 이유 또한 없으므로.
    path_thumb = models.CharField(max_length=255, default='', null=True, blank=True)
    
    # 참 거짓 필드
    enable = models.BooleanField(default=True)

    class Meta:
        ordering = ['title'] # 기본적으로 db에서 불러올 때 title 순으로 정렬