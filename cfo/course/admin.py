from django.contrib import admin
from .models import Course, Unit, Lesson, Activity


admin.site.register(Course)
admin.site.register(Unit)
admin.site.register(Lesson)
admin.site.register(Activity)
