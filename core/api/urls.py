from rest_framework import routers

from institutions.views import InstitutionViewSet, DomainViewSet, FacultyViewSet, DepartmentViewSet, CourseViewSet

app_name = 'apis'

router = routers.SimpleRouter()
router.register(r'institutions', InstitutionViewSet)
router.register(r'domains', DomainViewSet)
router.register(r'faculties', FacultyViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'courses', CourseViewSet)

urlpatterns = router.urls
