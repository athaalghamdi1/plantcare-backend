
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Plant
import json

def Home(request):
    if request.method == "GET":
        content = {'message': 'Welcome to the Plant Care api home route!'}
        return JsonResponse(content)

def login_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Login successful"})
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)

def signup_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already in use"}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password)
        return JsonResponse({"message": "Signup successful"})
    return JsonResponse({"error": "Invalid request method"}, status=405)

def plants_list(request):
    if request.user.is_authenticated:
        plants = Plant.objects.filter(user=request.user)
        plant_data = [{"id": plant.id, "name": plant.name, "reminder": plant.reminder} for plant in plants]
        return JsonResponse({"plants": plant_data})
    return JsonResponse({"error": "Unauthorized"}, status=401)

def plant_detail(request, id):
    if request.user.is_authenticated:
        try:
            plant = Plant.objects.get(id=id, user=request.user)
            plant_data = {"id": plant.id, "name": plant.name, "reminder": plant.reminder}
            return JsonResponse({"plant": plant_data})
        except Plant.DoesNotExist:
            return JsonResponse({"error": "Plant not found"}, status=404)
    return JsonResponse({"error": "Unauthorized"}, status=401)

def logout_view(request):
    logout(request)
    return JsonResponse({"message": "Logout successful"})
