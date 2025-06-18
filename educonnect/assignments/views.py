from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framwork.response import Response
from django.utils import timezone
from .models import Assignment, Submission
from .serializers import AssignmentSerializer, SubmissionSerializer, SubmissionCreateSerializer
from classes.models import Enrollment
# Create your views here.
class StudentAssignmentView(generics.ListAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Get Assignments from classes the student is logged in 
        enrolled_classes = Enrolement.objects.filter(
            student=self.request.user,
            status = 'enrolled'
        ).values_list('class_instance', flat=True)
        
        return Assignment.objects.filter(class_instance__in=enrolled_classes)
    
class TutorAssignmentView(generics.ListCreateAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Assignment.objects.filter(class_instance_tutor=self.request.user)    
    
class AssignmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    

@api_view
@permission_classes([permissions.IsAuthenticated])
def submit_assignment(request, assignment_id):
    try:
        assignment = Assignment.objects.get(id=assignment_id)
        
        # Check if the student is enrolled in the class
        if not Enrollment.objects.filter(
            student=request.user,
            class_instance=assignment.class_instance
            ).exists():