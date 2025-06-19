from django.contrib import admin
from .models import Class, Enrollment, Rating
# Register your models here.

@admin.register(Class)
class ClassAdmin (admin.ModelAdmin):
    list_display = ['title', 'tutor', 'subject', 'scheduled_at', 'status', 'enrolled_students_count']
    list_filter = ['status', 'subject', 'scheduled_at']
    search_fields = ['title', 'description', 'tutor_first_name', 'tutor_last_name']
    date_hierarchy = 'scheduled_at'
    
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'class_instance', 'enrolled_at', 'status']
    list_filter = ['status', 'enrolled_at']
    search_fields = ['student_first_name', 'student_last_name', 'class_instance_title']
    
@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['tutor', 'student', 'class_instance', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['tutor_first_name', 'tutor_last_name', 'student_first_name', 'student_last_name']
    
