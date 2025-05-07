from django.urls import path
from . import views

urlpatterns = [
    path("", views.Home, name="index"),
    path('users/signup/', views.CreateUserView.as_view(), name='signup'),
    path('users/login/', views.LoginView.as_view(), name='login'),
    path('users/token/refresh/', views.VerifyUserView.as_view(), name='token_refresh'),
    path("plants/", views.PlantAPIView.as_view(), name="plants_list"),
    path("plants/<int:plant_id>/", views.PlantDetail.as_view(), name="plant_detail"),
    path("recs/", views.RecommendationAPIView.as_view(), name="recommendations-list"),
    # path('due-reminders/', views.due_reminders, name='due-reminders'),
    # path('mark-as-watered/<int:pk>/', views.mark_as_watered, name='mark_as_watered'),
    # path('mark-as-fertilized/<int:pk>/', views.mark_as_fertilized, name='mark_as_fertilized'),
    # path("get-solution/", views.get_solution_by_symptom, name="get_solution"),

]
