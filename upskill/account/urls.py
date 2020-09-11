from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views

app_name = "account"

router = DefaultRouter()
router.register(r"users", views.UserViewset, basename="users")


urlpatterns = [
    path('api/', include(router.urls)),
]