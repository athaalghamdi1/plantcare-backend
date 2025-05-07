from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Plant, Recommendation
from rest_framework import generics, status
from rest_framework.views import APIView
from .serializers import PlantSerializer, UserSerializer, RecommendationSerializer
from datetime import date
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError
from django.db import IntegrityError


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
        print(request.data)
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            content = {'refresh': str(refresh), 'access': str(refresh.access_token),'user': UserSerializer(user).data}
            return Response(content, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=400)
    except Exception as err:
        return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VerifyUserView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            user = User.objects.get(username=request.user.username)
            try:
                refresh = RefreshToken.for_user(user)
                return Response({'refresh': str(refresh),'access': str(refresh.access_token),'user': UserSerializer(user).data}, status=status.HTTP_200_OK)
            except Exception as token_error:
                return Response({"detail": "Failed to generate token.", "error": str(token_error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as err:
            return Response({"detail": "Unexpected error occurred.", "error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    
# Model Views

class PlantAPIView(APIView):
    
    def get(self, request):
        plants = Plant.objects.filter(user=request.user)
        serializer = PlantSerializer(plants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = PlantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PlantDetail(APIView):     
    serializer_class = PlantSerializer     
    lookup_field = 'id'
    def get(self, request, plant_id):     
         try:     
             queryset = Plant.objects.get(id=plant_id)    
             plant = PlantSerializer(queryset)     
             return Response(plant.data, status=status.HTTP_200_OK)     
         except Exception as err:    
             return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
         
    def put(self, request, plant_id):
        try:
            plant = get_object_or_404(Plant, id=plant_id)
            serializer = self.serializer_class(plant, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, plant_id):
        try:
            plant = get_object_or_404(Plant, id=plant_id)
            plant.delete()
            return Response({'success': True}, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class RecommendationAPIView(APIView):
    def get(self, request):
        recommendations = Recommendation.objects.filter(user=request.user)
        serializer = RecommendationSerializer(recommendations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        print('request', request.data)
        serializer = RecommendationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RecommendationDetail(APIView):
    serializer_class = RecommendationSerializer
    lookup_field = 'id'
    def get(self, request, recommendation_id):
         try:
             queryset = Recommendation.objects.get(id=recommendation_id)
             recommendation = RecommendationSerializer(queryset)
             return Response(recommendation.data, status=status.HTTP_200_OK)
         except Exception as err:
             return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def put(self, request, recommendation_id):
        try:
            recommendation = get_object_or_404(Recommendation, id=recommendation_id)
            serializer = self.serializer_class(recommendation, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def delete(self, request, recommendation_id):
        try:
            recommendation = get_object_or_404(Recommendation, id=recommendation_id)
            recommendation.delete()
            return Response({'success': True}, status=status.HTTP_200_OK)
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


# def plant_detail(request, id):
#     if request.user.is_authenticated:
#         try:
#             plant = Plant.objects.get(id=id, user=request.user)
#             plant_data = {"id": plant.id, "name": plant.name, "reminder": plant.care_instructions}
#             return JsonResponse({"plant": plant_data})
#         except Plant.DoesNotExist:
#             return JsonResponse({"error": "Plant not found"}, status=404)
#     return JsonResponse({"error": "Unauthorized"}, status=401)



# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def due_reminders(request):
#     today = date.today()
#     plants = Plant.objects.filter(user=request.user)
#     reminders = []

#     for plant in plants:
#         if plant.last_watered and plant.watering_frequency_days:
#             days_since_water = (today - plant.last_watered).days
#             if days_since_water >= plant.watering_frequency_days:
#                 reminders.append(PlantSerializer(plant).data)

#     return Response(reminders)


# @api_view(['PATCH'])
# def mark_as_watered(request, pk):
#     plant = Plant.objects.get(id=pk, user=request.user)
#     plant.last_watered = date.today()
#     plant.save()
#     return Response({"message": "Plant watered successfully!"})

# @api_view(['PATCH'])
# def mark_as_fertilized(request, pk):
#     plant = Plant.objects.get(id=pk, user=request.user)
#     plant.last_fertilized = date.today()
#     plant.save()
#     return Response({"message": "Plant fertilized successfully!"})

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_recommendation(request, symptom):
#     recommendations = Recommendation.objects.filter(symptom__icontains=symptom)
#     if recommendations.exists():
#         return Response({"recommendations": [rec.solution for rec in recommendations]})
#     return Response({"message": "No recommendations found for the given symptom."})

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def get_solution_by_symptom(request):
#     data = json.loads(request.body)
#     symptom = data.get("symptom")
#     try:
#         recommendation = Recommendation.objects.get(symptom__icontains=symptom)
#         return Response({"solution": recommendation.solution})
#     except Recommendation.DoesNotExist:
#         return Response({"error": "No solution found for this symptom"}, status=404)
