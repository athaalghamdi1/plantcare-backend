from django.urls import path, include
from . import views
from .views import PlantViewSet, due_reminders, mark_as_watered, mark_as_fertilized
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'plants', PlantViewSet, basename='plant')

urlpatterns = [
    path("", views.Home, name="index"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("plants/", views.plants_list, name="plants_list"),
    path("plant/<int:id>/", views.plant_detail, name="plant_detail"),
    path("logout/", views.logout_view, name="logout"),
    path('api/', include(router.urls)),
    path('api/due-reminders/', due_reminders, name='due-reminders'),
    path('api/mark-as-watered/<int:pk>/', mark_as_watered, name='mark_as_watered'),
    path('api/mark-as-fertilized/<int:pk>/', mark_as_fertilized, name='mark_as_fertilized'),
]
