from rest_framework import serializers
from .models import Class, Enrollment, Rating
from accounts.serializers import UserSerializer

class ClassSerializer(serializers.ModelSerializer):
    """Serializer for Class model"""
    tutor = UserSerializer(read_only=True)
    enrolled_students_count = serializers.ReadOnlyField()
    is_enrolled = serializers.SerializerMethodField()
    
    class Meta:
        model = Class
        fields = [
            'id', 'tutor', 'title', 'description', 'subject',
            'scheduled_at', 'duration', 'max_students', 'price', 
            'status', 'meeting_link', 'enrolled_students_count',
            'is_enrolled', 'created_at', 'updated_at'
        ]
        read_only_fields = [ 'id', 'tutor', 'created_at', 'updated_at' ]
        
    def get_is_enrolled(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Enrollment.objects.filter(
                student=request.user,
                class_instance=obj,
                status='enrolled'
                ).exists()
        return False
    
    class ClassCreateSerializer(serializers.ModelSerializer):
        """Serializer for Class model creation"""
        class Meta:
            model = Class
            fields = [
                'title', 'description', 'subject', 'scheduled_at',
                'duration', 'max_students', 'price'
            ]
        def create(self, validated_data):
            """Create a new class instance"""
            validated_data['tutor']= self.context.get('request').user
            return super().create(validated_data)
class EnrollmentSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    class_instance = ClassSerializer(read_only=True)
    """Serializer for Enrollment model"""
    class Meta:
        model = Enrollment
        fields = [
            'id', 'student', 'class_instance', 'enrolled_at','status',
        ]
class RatingSerializer(serializers.ModelSerializer):
    """Serializer for Rating model"""
    student = UserSerializer(read_only=True)
    
    class Meta:
        model = Rating
        fields = ['id', 'student', 'comment', 'rating', 'created_at']
        