from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_dark_mode = models.BooleanField(default=False)
    language = models.CharField(max_length=10, choices=[('en', 'English'), ('ar', 'Arabic')], default='en')
    def __str__(self):
        return self.username
    
    
class Plant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plants')
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='plant_images/', null=True, blank=True)
    care_instructions = models.TextField(blank=True)
    def __str__(self):
        return self.name
    
    
class Analysis(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='analyses')
    result = models.TextField()
    analyzed_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Analysis for {self.plant.name} at {self.analyzed_at.strftime('%Y-%m-%d')}"
    
    
class Reminder(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='reminders')
    title = models.CharField(max_length=100)
    remind_at = models.DateTimeField()
    is_done = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.title} - {self.remind_at}"