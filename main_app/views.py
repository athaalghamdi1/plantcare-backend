from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
from .models import Plant, Recommendation, User
from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from .serializers import PlantSerializer, UserSerializer
from datetime import date
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import json
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError
from django.db import IntegrityError

class PlantViewSet(viewsets.ModelViewSet):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer


def Home(request):
    if request.method == "GET":
        content = {'message': 'Welcome to the Plant Care api home route!'}
        return JsonResponse(content)

# User Registration
class CreateUserView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  def create(self, request, *args, **kwargs):
    try:
      response = super().create(request, *args, **kwargs)
      user = User.objects.get(username=response.data['username'])
      refresh = RefreshToken.for_user(user)
      content = {'refresh': str(refresh), 'access': str(refresh.access_token), 'user': response.data }
      return Response(content, status=status.HTTP_200_OK)
    except (ValidationError, IntegrityError) as err:
      return Response({ 'error': str(err)}, status=status.HTTP_400_BAD_REQUEST)
  
class LoginView(APIView):
    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                content = {'refresh': str(refresh), 'access': str(refresh.access_token),'user': UserSerializer(user).data}
                return Response(content, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# def login_view(request):
#     if request.method == "POST":
#         data = json.loads(request.body)
#         email = data.get("email")
#         password = data.get("password")

#         user = authenticate(request, username=email, password=password)
#         if user is not None:
#             login(request, user)
#             return JsonResponse({"message": "Login successful"})
#         else:
#             return JsonResponse({"error": "Invalid credentials"}, status=400)
#     return JsonResponse({"error": "Invalid request method"}, status=405)


# def signup_view(request):
#     if request.method == "POST":
#         data = json.loads(request.body)
#         username = data.get("username")
#         email = data.get("email")
#         password = data.get("password")

#         if User.objects.filter(email=email).exists():
#             return JsonResponse({"error": "Email already in use"}, status=400)

#         user = User.objects.create_user(username=username, email=email, password=password)
#         return JsonResponse({"message": "Signup successful, please log in."})
#     return JsonResponse({"error": "Invalid request method"}, status=405)


# def plants_list(request):
#     # if request.user.is_authenticated:
#     plants = Plant.objects.all()
#     # plant_data = [{"id": plant.id, "name": plant.name, "reminder": plant.care_instructions} for plant in plants]
#     return JsonResponse({"plants": plants})
#     # return JsonResponse({"error": "Unauthorized"}, status=401)


def plant_detail(request, id):
    if request.user.is_authenticated:
        try:
            plant = Plant.objects.get(id=id, user=request.user)
            plant_data = {"id": plant.id, "name": plant.name, "reminder": plant.care_instructions}
            return JsonResponse({"plant": plant_data})
        except Plant.DoesNotExist:
            return JsonResponse({"error": "Plant not found"}, status=404)
    return JsonResponse({"error": "Unauthorized"}, status=401)


def logout_view(request):
    logout(request)
    return JsonResponse({"message": "Logout successful"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def due_reminders(request):
    today = date.today()
    plants = Plant.objects.filter(user=request.user)
    reminders = []

    for plant in plants:
        if plant.last_watered and plant.watering_frequency_days:
            days_since_water = (today - plant.last_watered).days
            if days_since_water >= plant.watering_frequency_days:
                reminders.append(PlantSerializer(plant).data)

    return Response(reminders)


@api_view(['PATCH'])
def mark_as_watered(request, pk):
    plant = Plant.objects.get(id=pk, user=request.user)
    plant.last_watered = date.today()
    plant.save()
    return Response({"message": "Plant watered successfully!"})

@api_view(['PATCH'])
def mark_as_fertilized(request, pk):
    plant = Plant.objects.get(id=pk, user=request.user)
    plant.last_fertilized = date.today()
    plant.save()
    return Response({"message": "Plant fertilized successfully!"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recommendation(request, symptom):
    recommendations = Recommendation.objects.filter(symptom__icontains=symptom)
    if recommendations.exists():
        return Response({"recommendations": [rec.solution for rec in recommendations]})
    return Response({"message": "No recommendations found for the given symptom."})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_solution_by_symptom(request):
    data = json.loads(request.body)
    symptom = data.get("symptom")
    try:
        recommendation = Recommendation.objects.get(symptom__icontains=symptom)
        return Response({"solution": recommendation.solution})
    except Recommendation.DoesNotExist:
        return Response({"error": "No solution found for this symptom"}, status=404)
