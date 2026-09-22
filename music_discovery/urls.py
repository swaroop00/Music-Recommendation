from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('', include("recommendations.urls")),
    path('', include("activities.urls")),
    path('api/analytics/', include("analytics.urls")),

]
