from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import (
    Institution, Domain, Faculty, Department, Course,
    Section, Instructor, TeachingAssistant, UserEmail
)
from .permissions import IsAdminOrReadOnly
from .serializers import (
    InstitutionSerializer, DomainSerializer, FacultySerializer,
    DepartmentSerializer, CourseSerializer, SectionSerializer,
    InstructorSerializer, TeachingAssistantSerializer, UserEmailSerializer
)


# Create your views here.


class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    permission_classes = [IsAdminOrReadOnly]


class DomainViewSet(viewsets.ModelViewSet):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    permission_classes = [IsAdminOrReadOnly]


class FacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    permission_classes = [IsAdminOrReadOnly]


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAdminOrReadOnly]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdminOrReadOnly]


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticated]


class InstructorViewSet(viewsets.ModelViewSet):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer
    permission_classes = [IsAuthenticated]


class TeachingAssistantViewSet(viewsets.ModelViewSet):
    queryset = TeachingAssistant.objects.all()
    serializer_class = TeachingAssistantSerializer
    permission_classes = [IsAuthenticated]


class UserEmailViewSet(viewsets.ModelViewSet):
    queryset = UserEmail.objects.all()
    serializer_class = UserEmailSerializer
    permission_classes = [IsAuthenticated]
