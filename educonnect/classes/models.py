from django.db import models
from django.conf import settings
# Create your models here.

class Class(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('live', 'Live'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    tutor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='taught_classes', 
        
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    subject = models.CharField(max_length=100)
    scheduled_at = models.DateTimeField()
    duration = models.PositiveBigIntegerField(help_text="Duration in minutes")
    max_students = models.PositiveBigIntegerField(default=25)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='scheduled')
    meeting_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-scheduled_at']
    
    def __str__(self):
        return f"{self.title} - {self.tutor.get_full_name()}"
    
    @property
    def enrolled_students_count(self):
        return self.enrollments.filter(status='enrolled').count()
    
class Enrollment(models.Model):
    # class STATUS_CHOICES(models.TextChoices):
    #     ENROLLED = 'enrolled', 'Enrolled'
    #     WAITLIST = 'waitlist', 'Waitlist'
    #     CANCELLED = 'cancelled', 'Cancelled'
    #     COMPLETED = 'completed', 'Completed'
    STATUS_CHOICES = [
        ('enrolled', 'Enrolled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    student= models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments',
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='enrolled')
    
    class Meta:
        unique_together = ['student', 'class_instance']
        
    def __str__(self):
        return f"{self.student.get_full_name()} - {self.class_instance.title}"
    
class Rating(models.Model):
    tutor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_ratings',
    )
    # rating = models.CharField(max_length=10, choices=Rating.RATING_CHOICES, default='')
    # rating = models.IntegerField(choices=Rating.RATING_CHOICES, default=0)
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='given_ratings',
    )
    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE)
    rating = models.PositiveBigIntegerField(choices=[(i, i) for i in range (1, 6)], default=0)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['tutor', 'student', 'class_instance']
        
    def __str__(self):
        return f"{self.rating} stars - {self.tutor.get_full_name()}"
