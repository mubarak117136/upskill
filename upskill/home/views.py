from django.shortcuts import render

from rest_framework.views import View
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView

from django_filters import rest_framework as filters
from rest_framework import filters as drf_filters


from . import models
from . import serializers
from . import permissions



class MovieFilter(filters.FilterSet):
    name = filters.CharFilter(method="name_filter")

    def name_filter(self, queryset, name, value):
        return queryset.filter(name__icontains=value)

    class Meta:
        model = models.Movie
        fields = ["name", ]


class MovieViewset(viewsets.ModelViewSet):
    queryset = models.Movie.objects.all()
    permission_classes = (permissions.MoviePermission, )
    
    filter_backends = (filters.DjangoFilterBackend, drf_filters.SearchFilter)
    search_fields = ["name", ]
    filterset_class = MovieFilter

    
    def get_serializer_class(self):
        if self.action == "list":
            return serializers.FlatMovieSerializer
        elif self.action == "rate":
            return serializers.RatingSerializer
        return serializers.MovieSerializer
    
    @action(
        detail=True, 
        methods=["post"],
        serializer_class=serializers.RatingSerializer
    )
    def rate(self, request, pk=None):
        movie = models.Movie.objects.get(id=pk)
        user = request.user
        rating = request.data.get("rating", 0)
        
        models.Rating.objects.create(
            user=user,
            movie=movie,
            rating=rating
        )
        return Response({
            "description": "You rated successfully!"
        }, status=status.HTTP_201_CREATED)
        
        

class RatingViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.FlatRatingSerializer
    queryset = models.Rating.objects.all()
    permission_classes = (permissions.MoviePermission, )
    
    # def get_serializer_class(self):
    #     if self.action == "list":
    #         return serializers.FlatRatingSerializer
    #     return ""
    