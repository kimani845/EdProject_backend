from django.db import models
from django.conf import settings
from classes.models import Class     

# Create your models here.

class Assignment(models.Model):
    class_instance = models.Foreignkey(Class, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    max_score = models.PositiveBigIntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-due_at']
        
    def __str__(self):
        return f"{self.title} - {self.class_instance.title}"
    
class Submission (models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to='submissions', blank=True, null=True)
    score = models.PositiveBigIntegerField(default=0)
    feedback = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    graded_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        unique_together = ['assignment', 'student']
        
    def __str__(self):
        return f"{self.student.get_full_name()} - {self.assignment.title}"
    
    @property
    def status(self):
        if self.score is not None:
            return 'graded'
        elif self.submitted_at is not None:
            return 'submitted'
        else:
            return 'not submitted'
