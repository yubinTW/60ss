from django.db import models

# Create your models here.
class Podcasts(models.Model):
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=255,blank=False)
    date = models.CharField(max_length=20,blank=True)
    audio = models.CharField(max_length=255)
    img = models.CharField(max_length=255,blank=True)
    transcript = models.TextField(blank=True)