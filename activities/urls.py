from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserActivityViewSet

router = DefaultRouter()
router.register(
    "activity",
    UserActivityViewSet,
    basename="activity"
)

urlpatterns = [
    path("api/", include(router.urls)),
]
    