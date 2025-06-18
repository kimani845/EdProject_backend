# This serializer file converts data into json
from rest_framework import serializers
from django.conrib.auth import authenticate
from .models import User, TutorProfile, StudentProfile

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.Charfield(write_only=True)
    subjects = serializers.ListField(
        child=serializers.CharField(max_length=50),
        required = False,
        allow_empty = True
    )
    
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password_confirm',
            'first_name',
            'last_name',
            'phone',
            'role',
            'bio',
            'subjects'
        ]
        
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return attrs
    def create (self, validated_data):
        validated_data.pop('password_confirm')
        subjects = validated_data.pop('subjects')
        
        user = User.objects.create_user(**validated_data)
        if user.role == 'tutor':
            TutorProfile.objects.create(user=user, subjects=subjects)
        else:
            StudentProfile.objects.create(user=user)
            
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)
    
    def validate (self, attrs):
        email = attrs.get['email']
        password = attrs.get['password']
        
        if email and password:
            try:
                user = User.objects.get(email=email)
                user = authenticate(username=user.username, password=password)
                if not user:
                    raise serializers.ValidationError({'email': 'Invalid email or password.'})
            except User.DoesNotExist:
                raise serializers.ValidationError({'email': 'Invalid email or password.'})
        else:
            raise serializers.ValidationError('Must provide both email and password')
        
        attrs ['user'] = user
        return attrs
    
class TutorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorProfile
        fields = [
            'subjects',
            'ratings',
            'total_ratings',
            'verified'
        ]
        
class StudentProfileSerializer(serializer.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = [
            'grade_level',
            'School'
        ]
        
class UserSerializer(serializers.ModelSerializer):
    tutor_profile = TutorProfileSerializer(read_only=True)
    student_profile = StudentProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'phone',
            'role',
            'bio',
            'avatar',
            'created_at'
            'tutor_profile',
            'student_profile',
        
        ]
        
        read_only_fields = ['id', 'username', 'created_at']
            
        
