from django.urls import path, include
from . import views
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path("", views.Home, name="index"),
    # path("login/", views.login_view, name="login"),
    # path("signup/", views.signup_view, name="signup"),
    path('users/signup/', views.CreateUserView.as_view(), name='signup'),
    path('users/login/', views.LoginView.as_view(), name='login'),
    # path("plants/", views.plants_list, name="plants_list"),
    path("plants/", views.PlantAPIView.as_view(), name="plants_list"),
    path("plant/<int:id>/", views.plant_detail, name="plant_detail"),
    path("logout/", views.logout_view, name="logout"),
    path('', include(router.urls)),
    path('due-reminders/', due_reminders, name='due-reminders'),
    path('mark-as-watered/<int:pk>/', mark_as_watered, name='mark_as_watered'),
    path('mark-as-fertilized/<int:pk>/', mark_as_fertilized, name='mark_as_fertilized'),
    path("get-solution/", views.get_solution_by_symptom, name="get_solution"),

]
