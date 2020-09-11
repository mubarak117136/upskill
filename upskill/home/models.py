from django.db import models
from django.contrib.auth import get_user_model

USER = get_user_model()

class RatingChoice(models.TextChoices):
    G = "G", "General Audiences"
    PG = "PG", "Parental Guidance Suggested"
    PG_13 = "PG-13", "Parents Strongly Cautioned"
    R = "R", "Restricted"
    NC_17 = "NC-17", "Adults Only"

class Movie(models.Model):
    user = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        related_name="movies",
        null=True
    )
    name = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    rating = models.CharField(
        max_length=50, 
        choices=RatingChoice.choices, 
        default=RatingChoice.G, 
        null=True, 
        blank=True
    )
    release_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class Rating(models.Model):
    user = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        related_name="ratings",
        null=True
    )
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="ratings"
    )
    rating = models.FloatField(default=0.0)
    
    def __str__(self):
        return str(self.user) + " : " + str(self.movie)