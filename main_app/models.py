from django.db import models
from django.contrib.auth.models import User

RECOMMENDATION_SOLUTION_PAIRS = (
    ("Yellow leaves", "Reduce watering frequency."),
    ("Brown tips", "Increase humidity slightly."),
    ("Wilting", "Check soil moisture."),
    ("Leaf drop", "Avoid cold drafts."),
    ("Moldy soil", "Improve air circulation."),
    ("Leggy growth", "Provide more light."),
    ("Pale leaves", "Add liquid fertilizer."),
    ("Sticky leaves", "Treat for pests."),
    ("Root rot", "Repot in dry soil."),
    ("Spots on leaves", "Remove affected leaves."),
    
)
RECOMMENDATION_CHOICES = [ (symptom, symptom) for symptom, _ in RECOMMENDATION_SOLUTION_PAIRS ]
SYMPTOM_TO_SOLUTION = dict(RECOMMENDATION_SOLUTION_PAIRS)
    
class Plant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.URLField(max_length=500, blank=True)
    last_watered = models.DateField()
    watering_frequency_days = models.IntegerField(default=3)
    last_fertilized = models.DateField(null=True, blank=True)
    fertilizing_frequency_days = models.IntegerField(default=14)

    def __str__(self):
        return self.name
    
    
# class Analysis(models.Model):
#     plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='analyses')
#     result = models.TextField()
#     analyzed_at = models.DateTimeField(auto_now_add=True)
#     def __str__(self):
#         return f"Analysis for {self.plant.name} at {self.analyzed_at.strftime('%Y-%m-%d')}"
    
    
class Reminder(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='reminders')
    title = models.CharField(max_length=100)
    remind_at = models.DateTimeField()
    is_done = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.title} - {self.remind_at}"
    
    
class Recommendation(models.Model):
    symptom = models.CharField(max_length=255, choices=RECOMMENDATION_CHOICES)    
    solution = models.TextField(blank=True)
    def save(self, *args, **kwargs):
            # Automatically set the solution before saving
            self.solution = SYMPTOM_TO_SOLUTION.get(self.symptom, "")
            super().save(*args, **kwargs)
            
    def __str__(self):
        return f"Symptom: {self.symptom}, Solution: {self.solution}"
