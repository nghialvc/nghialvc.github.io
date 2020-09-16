from django.db import models
from django.conf import settings

# Create your models here.

class MangaType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class MangaInfo(models.Model):
    name = models.CharField(max_length=500)
    author = models.CharField(max_length = 200)
    manga_type = models.ForeignKey(MangaType, on_delete=models.CASCADE)
    description = models.TextField(null=True)
    current_chap = models.IntegerField(default=1)
    avatar = models.ImageField(null=True)
    time_up = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name+" - Chap "+str(self.current_chap)

class ChapInfo(models.Model):
    name = models.CharField(max_length=200)
    chap = models.IntegerField(default=1)
    content = models.ImageField(null=True)

    def __str__(self):
        return self.name +" - "+ str(self.chap)
