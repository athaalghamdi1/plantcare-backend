# main_app/urls.py
from django.urls import path
from .views import UserDetailView, PlantListView, PlantDetailView, AnalysisListView, ReminderListView, ReminderDetailView, HomePageView
from .views import LoginView, TokenRefreshView
urlpatterns = [
    path('HomePage/',HomePageView.as_view(), name='HomePage'),
    path('users/', UserDetailView.as_view(), name='user-detail'),
    path('plants/', PlantListView.as_view(), name='plant-list'),
    path('plants/<int:pk>/', PlantDetailView.as_view(), name='plant-detail'),
    path('analyses/', AnalysisListView.as_view(), name='analysis-list'),
    path('reminders/', ReminderListView.as_view(), name='reminder-list'),
    path('reminders/<int:pk>/', ReminderDetailView.as_view(), name='reminder-detail'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]






