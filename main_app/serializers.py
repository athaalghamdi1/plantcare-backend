from rest_framework import serializers
from .models import Plant, Reminder, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = '__all__'


# class AnalysisSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Analysis
#         fields = '__all__'

class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = '__all__'
