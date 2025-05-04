# main_app/views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Plant, User, Analysis, Reminder
from .serializers import PlantSerializer, UserSerializer, AnalysisSerializer, ReminderSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
class PlantListView(generics.ListCreateAPIView):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
class PlantDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer
    permission_classes = [IsAuthenticated]
class AnalysisListView(generics.ListCreateAPIView):
    queryset = Analysis.objects.all()
    serializer_class = AnalysisSerializer
    permission_classes = [IsAuthenticated]
class ReminderListView(generics.ListCreateAPIView):
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer
    permission_classes = [IsAuthenticated]
class ReminderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer
    permission_classes = [IsAuthenticated]
    
# class HomePageView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = HomePage.objects.all()
#     serializer_class = HomePageSerializer
#     permission_classes = [IsAuthenticated]
    
class LoginView(TokenObtainPairView):
    pass
class TokenRefreshView(TokenRefreshView):
    pass