from rest_framework import serializers

from . import models


class FlatMovieSerializer(serializers.ModelSerializer):
    release_date = serializers.SerializerMethodField()
    
    class Meta:
        model = models.Movie
        fields = (
            "id",
            "name",
            "genre",
            "rating",
            "release_date"
        )
    
    def get_release_date(self, obj):
        return obj.release_date.strftime("%d-%m-%Y")

class MovieSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    average_rating = serializers.SerializerMethodField()
    
    def get_average_rating(self, obj):
        total_rating = sum([r.rating for r in obj.ratings.all()])
        num_of_rating = obj.ratings.count()
        return round(total_rating/num_of_rating, 1)
    
    class Meta:
        model = models.Movie
        fields = "__all__"
        

class FlatRatingSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    movie_id = serializers.IntegerField(source="movie.id", read_only=True)
    
    class Meta:
        model = models.Rating
        fields = (
            "id",
            "user_id",
            "movie_id",
            "rating"
        )

class RatingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Rating
        fields = ("rating", )