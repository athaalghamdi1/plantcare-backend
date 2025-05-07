from rest_framework import serializers
from .models import Plant, Reminder, Recommendation
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    # Add a password field, make it write-only
    # prevents allowing 'read' capabilities (returning the password via api response)
    password = serializers.CharField(write_only=True)  

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']  
        )
      
        return user

class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = ['id', 'name', 'last_watered', 'last_fertilized']


class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        # fields = '__all__'
        fields =['plant', 'symptom', 'solution']


class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = '__all__'

