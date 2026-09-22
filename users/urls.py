from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet

router = DefaultRouter()
router.register("users", UserProfileViewSet, basename="user-profile")

urlpatterns = [
    path('api/', include(router.urls)),
]
