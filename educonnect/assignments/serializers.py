from rest_framework import serializers
from .models import Assignment, Submission
from account.serializers import UserSerializer

class AssignmentSerializer(serializers.ModelSerializer):
    class_title = serializers.CharField(source='class_instance_title', read_only=True)
    subject = serializers.CharField(source='class_instance_subject', read_only=True)
    
    class Meta:
        model = Assignment
        fields = [
            'id', 'title','description', 'due_date','max_score', 
            'class_title', 'subject', 'created_at', 'updated_at'
        ]
        
class SubmissionSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    assignment = AssignmentSerializer(read_only=True)
    status = serializers.CharField()
    
    class Meta:
        model = Submission
        fields = [
            'id', 'assignment', 'student', 'content', 'file', 
            'score', 'feedback', 'submitted_at', 'graded_at', 'status'
        ]
        readonly_fields = ['id', 'student', 'submitted_at', 'graded_at']
        
class SubmissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['content', 'file']
        
    def create(self, validated_data):
        validated_data['student']=self.context['request'].user
        validated_data['assignment']=self.context['assignment']
        return super().create(validated_data)