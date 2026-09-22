from django.urls import path

from analytics.views import AnalyticsSummaryView, AnalyticsTrendsView, UserAnalyticsView

urlpatterns = [
    path("summary/", AnalyticsSummaryView.as_view()),
    path("trends/", AnalyticsTrendsView.as_view()),
    path("user/<int:user_id>/", UserAnalyticsView.as_view()),
]