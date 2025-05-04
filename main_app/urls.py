from django.urls import path
from . import views

urlpatterns = [
    path("", views.Home, name="index"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("plants/", views.plants_list, name="plants_list"),
    path("plant/<int:id>/", views.plant_detail, name="plant_detail"),
    path("logout/", views.logout_view, name="logout"),
]
