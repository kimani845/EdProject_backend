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
        return Class.objects.filter(enrollment__student=self.request.user)

    
        