from rest_framework import serializers

from .models import (
    Institution, Domain, Faculty, Department, Course, UserEmail,
    Section, Instructor, TeachingAssistant
)


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = '__all__'


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = '__all__'


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = '__all__'

    def validate(self, attrs):
        if TeachingAssistant.objects.filter(
            first_name=attrs['first_name'],
            last_name=attrs['last_name'],
            department=attrs['department']
        ).exists():
            raise serializers.ValidationError('An instructor with the same name and department already exists.')
        return attrs


class TeachingAssistantSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeachingAssistant
        fields = '__all__'

    def validate(self, attrs):
        if TeachingAssistant.objects.filter(
            first_name=attrs['first_name'],
            last_name=attrs['last_name'],
            department=attrs['department']
        ).exists():
            raise serializers.ValidationError('A teaching assistant with the same name and department already exists.')
        return attrs


class UserEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEmail
        fields = '__all__'

    def validate_email(self, value):
        domain = value.split('@')[1]
        if UserEmail.objects.filter(email=value).exists():
            raise serializers.ValidationError('An account with this email already exists.')
        if not Domain.objects.filter(name=domain).exists():
            return serializers.ValidationError('This domain is not currently supported.')
        return value

    def create(self, validated_data):
        email = UserEmail(
            email=validated_data['email'],
            user=validated_data['user'],
            domain=Domain.objects.get(name=validated_data['email'].split('@')[1])
        )
        email.save()
        return email
