from django.contrib import admin
from .models import Plant, Reminder, Recommendation, User

admin.site.register(Plant)
admin.site.register(Reminder)
admin.site.register(Recommendation)
admin.site.register(User)

