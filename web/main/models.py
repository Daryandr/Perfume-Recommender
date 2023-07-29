from django.db import models


class Perfume(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.TextField()
    image_url = models.TextField()
    average_rating = models.FloatField()
    ratings_count = models.IntegerField()
    weighted_rating = models.FloatField()
    accords = models.TextField()
    notes = models.TextField()
    year = models.IntegerField()
    season = models.TextField()
    longevity = models.TextField()


class Users(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    likes = models.TextField()
    dislike = models.TextField()


