from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views

app_name = "home"

router = DefaultRouter()
router.register(r"movies", views.MovieViewset, basename="movies")
router.register(r"ratings", views.RatingViewset, basename="movies")

urlpatterns = [
    path('api/', include(router.urls)),
]