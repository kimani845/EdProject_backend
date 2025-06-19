from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Class, Enrollment, Rating
from .serializers import (
    ClassSerializer, ClassCreateSerializer,
    EnrollmentSerializer, RatingSerializer
    )

# Create your views here.
class ClassListCreateView(generics.ListCreateView):
    queryset = Class.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['subject', 'status', 'tutor']
    search_fields = ['title','subject', 'description']
    ordering_fields = ['scheduled_at', 'created_at', 'price']
    ordering = ['-scheduled_at']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ClassCreateSerializer
        return ClassSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny]
    
class DetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny]
        return [permissions.IsAuthenticated]
class TutorClassView(generics.ListAPIView):
    serializer_class = ClassSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Class.objects.filter(tutor=self.request.user)
    
class StudentClassView(generics.ListAPIView):
    serializer_class = ClassSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        enrollments = Enrollment.objects.filter(
            student=self.request.user,
            status = 'enrolled'
            ).values_list('class_instance', flat=True)
        return Class.objects.filter(id__in=enrollments)
    
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def enroll_in_class(request, class_id):
    try:
        class_instance = Class.objects.get(id=class_id)
        
        # Check if already enrolled
        if Enrollment.objects.filter(
            student=request.user,
            class_instance=class_instance
        ).exists():
            return Response(
                {'error': 'Already enrolled in this Class'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Check if the class is full
        if class_instance.enrolled_student_count >= class_instance.max_students:
            return Response(
                {'error': 'Class is full'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        enrollment = Enrollment.objects.create(
            student=request.user,
            class_instance=class_instance
        )
        return Response(
            EnrollmentSerializer(enrollment).data, 
            class_instance = class_instance
        )
    except Class.DoesNotExist:
        return Response(
            {'error': 'Class does not exist'},
            status=status.HTTP_404_NOT_FOUND
        )
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def rate_tutor(request, class_id):
    try:
        class_instance = Class.objects.get(id=class_id)
        
        # Check if the student was enrolled in this class
        if not Enrollment.objects.filter(
            student=request.user,
            class_instance=class_instance,
            status_in =['enrolled', 'attended']
        ).exists():
            return Response(
                {'error': 'You are not enrolled in this class'},
                status=status.HTTP_400
            )
        rating_data = request.data.copy()
        rating_data['tutor'] = class_instance.tutor.id
        rating_data['class_instance'] = class_instance.id
        
        # Check if already rated
        existing_rating = Rating.objects.filter(
            student=request.user,
            tutor=class_instance.tutor,
            class_instance=class_instance
        ).first()
        
        if existing_rating:
            serializer = RatingSerializer(existing_rating, data=rating_data, partial=True)
        else:
            serializer = RatingSerializer(data=rating_data)
        
        if serializer.is_valid:
            rating=serializer.save(
                student=request.user,
                tutor=class_instance.tutor,
                class_instance=class_instance
            )
            
            # update tutor's average rating'
            tutor_profile = class_instance.tutor.tutor_profile
            ratings = Rating.objects.filter(tutor=class_instance.tutor)
            avg_rating = sum(rating.rating for rating in ratings) / len(ratings)
            tutor_profile.rating = round(avg_rating, 2)
            tutor_profile.total_rating= len(ratings)
            tutor_profile.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Class.DoesNotExist:
        return Response(
            {'error': 'Class does not exist'},
            status=status.HTTP_404_NOT_FOUND
        )
            
    
        