from django.urls import path

from rest_framework import routers

from institutions.views import (
    InstitutionViewSet, DomainViewSet, CourseViewSet,
    UserEmailViewSet, InstructorViewSet, TeachingAssistantViewSet
)
app_name = 'apis'

router = routers.SimpleRouter()
router.register(r'institutions', InstitutionViewSet)
router.register(r'domains', DomainViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'useremail', UserEmailViewSet, basename='useremail')
router.register(r'instructors', InstructorViewSet)
router.register(r'teaching-assistants', TeachingAssistantViewSet)

urlpatterns = router.urls
