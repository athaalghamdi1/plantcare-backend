from rest_framework import serializers
from .models import Plant, User, Analysis, Reminder

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_dark_mode', 'language']
class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = ['id', 'user', 'name', 'image', 'care_instructions']
class AnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis
        fields = ['id', 'plant', 'result', 'analyzed_at']
class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = ['id', 'plant', 'title', 'remind_at', 'is_done']