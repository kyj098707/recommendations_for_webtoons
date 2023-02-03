from django.db import models

# Create your models here.
class Detail(models.Model):
    title_id = models.CharField(max_length=15, blank=True, null=True)
    title = models.CharField(max_length=20, blank=True, null=True)
    website = models.CharField(max_length=10, blank=True, null=True)
    story = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detail'