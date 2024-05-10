from django.conf import settings
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.core.mail import send_mail
from django.views import View

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import (
    Institution, Domain, Course,
    Instructor, TeachingAssistant, UserEmail
)
from .permissions import IsAdminOrReadOnly
from .serializers import (
    InstitutionSerializer, DomainSerializer, CourseSerializer,
    InstructorSerializer, TeachingAssistantSerializer, UserEmailSerializer
)


# Create your views here.


class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    permission_classes = [AllowAny]


class DomainViewSet(viewsets.ModelViewSet):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    permission_classes = [AllowAny]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdminOrReadOnly]


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

    @action(detail=True, methods=['get'])
    def verify(self, request, pk=None):
        user_email = get_object_or_404(UserEmail, pk=pk)

        verification_token = request.query_params.get('verification_token', None)

        if verification_token == user_email.verification_token:
            user_email.status = UserEmail.STATUS_VERIFIED
            user_email.save()

            return Response({'status': 'Email verified'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': f'Invalid verification token: {request.data.get("verification_token")}'}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)

        user_email = serializer.instance

        verification_link = request.build_absolute_uri(reverse('useremail-verify', args=[user_email.id]) + f'?verification_token={user_email.verification_token}')
        print(verification_link)
        send_mail(
            'Verify Email',
            f'Click the link to verify your email: {verification_link}',
            settings.DEFAULT_FROM_EMAIL,
            [user_email.email],
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
