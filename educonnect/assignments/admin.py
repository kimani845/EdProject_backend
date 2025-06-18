from django.contrib import admin
from .models import Assignment, Submission

# Register your models here.

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['assignment', 'student', 'submitted_at', 'grade', 'status']
    list_filter = ['submitted_at', 'graded_at']
    search_fields = ['student__first_name', 'student__last_name', 'assignment__title']
