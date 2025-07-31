from django.db import models

# Create your models here.
class Movie(models.Model):
    imdb_id = models.CharField(max_length=15, unique=True)
    title = models.CharField(max_length=255)
    titleType = models.CharField(max_length=255, default='movie')
    year = models.IntegerField(null=True)
    runtime_minutes = models.IntegerField(null=True)
    genres = models.CharField(max_length=255)
    average_rating = models.FloatField(null=True)
    num_votes = models.IntegerField(null=True),
    isAdult = models.BooleanField(null=True)

    def __str__(self):
        return self.title

