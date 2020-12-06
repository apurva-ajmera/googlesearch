from django.db import models
from django.utils import timezone

class Website(models.Model):
    url = models.CharField(max_length=100)

    def __str__(self):
        return self.url

class WebPage(models.Model):
    url = models.CharField(max_length=100)
    root = models.ForeignKey(Website, on_delete=models.CASCADE)
    visited = models.BooleanField(blank=True)
    scrapy = models.BooleanField(blank=True)
    last_updated = models.DateTimeField(blank=True, default=timezone.now)
    last_crawled = models.DateTimeField(blank=True, default=timezone.now)
    click_ratio = models.IntegerField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    owner = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.url

class Backward_Index(models.Model):
    data = models.CharField(max_length=100)
    urls = models.TextField()

    def __str__(self):
        return self.data
