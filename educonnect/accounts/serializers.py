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