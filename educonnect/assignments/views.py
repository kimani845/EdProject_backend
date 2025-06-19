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
        enrolled_classes = Enrollement.objects.filter(
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
            class_instance=assignment.class_instance,
            status= 'enrolled'
        ).exists():
            return Response(
                {'error': 'You are not enrolled in this class'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if already submitted
        existing_Submission = Submission.objects.filter(
            student=request.user,
            assignment=assignment
            ).first()
        if existing_Submission:
            # Update the Existing submission
            serializer = SubmissionSerializer(
                existing_Submission,
                data=request.data,
                partial=True,
                context={'request': request, 'assignment': assignment}
            )
        else:
            # Create a new submission
            serializer = SubmissionSerializer(
                data=request.data, 
                context={'request': request, 'assignment': assignment}
            )
        
        if serializer.is_valid():
            submission=serializer.save()
            return Response(
                {'submission':SubmissionSerializer(submission).data},
                status=status.HTTP_201_CREATED
            )
            
        return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
    except Assignment.DoesNotExist:
        return Response(
            {'error': 'Assignment not found'},
            status=status.HTTP_404_NOT_FOUND
        )
        
# View to allow tutors get assignments
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_submission(request, assingment_id):
    try:
        assignment = Assignment.objects.get(id=assingment_id)
        
        # Check if user is the tutor of this assignment's class
        if assignment.class_instance.tutor != request.user:
            return Response(
                {'error': 'You are not the tutor of this class'},
                status=status.HTTP_FORBIDDEN
            )
        submissions = Submission.objects.filter(assignment=assignment)
        serializer = SubmissionSerializer(submissions, many=True)
        
        return Response(serializer.data)
    except Assignment.DoesNotExist:
        return Response(
            {'error': 'Assignment not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def grade_submission(request, submission_id):
    try:
        submission = Submission.objects.get(id=submission_id)
    
    # Check if the user is a tutor
        if submission.assignment.class_instance.tutor != request.user:
            return Response(
                {'error': 'Permission denied, you cannot grade this assignment'},
                status=status.HTTP_403_FORBIDDEN
            )
        score = request.data.get('score')
        feedback = request.data.get('feedback', '')
        
        if score is not none:
            submission.score = score
            submission.feedback = feedback
            submission.graded_at = timezone.now()
            submission.save()
            return Response(\
                {'message': 'Submission graded successfully'},
                status=status.HTTP_200_OK
            )
        return Response(
            {'error': 'Score is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Submission.DoesNotExist:
        return Response(
            {'error': 'Submission not found'},
            status=status.HTTP_404_NOT_FOUND
        )