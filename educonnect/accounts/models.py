from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = [
        # ('admin', 'Admin'),
        ('student', 'student'),
        ('tutor', 'tutor'),
    ]
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    # is_active = models.BooleanField(default=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user_name})"
    
class TutorProfile(models.model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name= 'tutor_profile')
    subjects = models.JSONField(default=list, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_ratings = models.PositiveBigIntegerField(default=0)
    verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Tutor Profile - {self.user.get_full_name}"
    
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    grade_level = models.CharField(max_length=50, blank=True, null=True)
    school = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"Student Profile - {self.user.get_full_name}"
    