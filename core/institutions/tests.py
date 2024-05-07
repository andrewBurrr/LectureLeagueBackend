from django.test import TestCase
from rest_framework.test import APIClient
from .models import (
    Institution, Domain, Faculty, Department, Course,
    Section, Instructor, TeachingAssistant, UserEmail
)

# Create your tests here.

class InstitutionViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.institution = Institution.objects.create(name='Test Institution')
    
    def test_list_institutions(self):
        response = self.client.get('/institutions/institutions/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], 'Test Institution')

    def test_retrieve_institution(self):
        response = self.client.get(f'/institutions/institutions/{self.institution.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Test Institution')


class DomainViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.institution = Institution.objects.create(name='Test Institution')
        self.domain = Domain.objects.create(name='Test Domain', institution=self.institution)

    def test_list_domains(self):
        response = self.client.get('/institutions/domains/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], 'Test Domain')

    def test_retrieve_domain(self):
        response = self.client.get(f'/institutions/domains/{self.domain.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Test Domain')

class FacultyViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.institution = Institution.objects.create(name='Test Institution')
        self.faculty = Faculty.objects.create(name='Test Faculty', institution=self.institution)
                                              
    def test_list_faculties(self):
        response = self.client.get('/institutions/faculties/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], 'Test Faculty')
    
    def test_retrieve_faculty(self):
        response = self.client.get(f'/institutions/faculties/{self.faculty.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Test Faculty')


class DepartmentViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.institution = Institution.objects.create(name='Test Institution')
        self.faculty = Faculty.objects.create(name='Test Faculty', institution=self.institution)
        self.department = Department.objects.create(name='Test Department', faculty=self.faculty)

    def test_list_departments(self):
        response = self.client.get('/institutions/departments/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], 'Test Department')

    def test_retrieve_department(self):
        response = self.client.get(f'/institutions/departments/{self.department.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Test Department')



class CourseViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.institution = Institution.objects.create(name='Test Institution')
        self.faculty = Faculty.objects.create(name='Test Faculty', institution=self.institution)
        self.department = Department.objects.create(name='Test Department', faculty=self.faculty)
        self.course = Course.objects.create(name='Test Course', department=self.department)

    def test_list_courses(self):
        response = self.client.get('/institutions/courses/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], 'Test Course')

    def test_retrieve_course(self):
        response = self.client.get(f'/institutions/courses/{self.course.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Test Course')



class SectionViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.institution = Institution.objects.create(name='Test Institution')
        self.faculty = Faculty.objects.create(name='Test Faculty', institution=self.institution)
        self.department = Department.objects.create(name='Test Department', faculty=self.faculty)
        self.course = Course.objects.create(name='Test Course', department=self.department)
        self.section = Section.objects.create(name='Test Section', course=self.course)

    def test_list_sections(self):
        response = self.client.get('/institutions/sections/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], 'Test Section')

    def test_retrieve_section(self):
        response = self.client.get(f'/institutions/sections/{self.section.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Test Section')



class InstructorViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.institution = Institution.objects.create(name='Test Institution')
        self.faculty = Faculty.objects.create(name='Test Faculty', institution=self.institution)
        self.department = Department.objects.create(name='Test Department', faculty=self.faculty)
        self.instructor = Instructor.objects.create(first_name='Test', last_name='Instructor', department=self.department)
    
    def test_list_instructors(self):
        response = self.client.get('/institutions/instructors/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['first_name'], 'Test')
        self.assertEqual(response.data[0]['last_name'], 'Instructor')
    
    def test_retrieve_instructor(self):
        response = self.client.get(f'/institutions/instructors/{self.instructor.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['first_name'], 'Test')
        self.assertEqual(response.data['last_name'], 'Instructor')
    


class TeachingAssistantViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.institution = Institution.objects.create(name='Test Institution')
        self.faculty = Faculty.objects.create(name='Test Faculty', institution=self.institution)
        self.department = Department.objects.create(name='Test Department', faculty=self.faculty)
        self.ta = TeachingAssistant.objects.create(first_name='Test', last_name='TA', department=self.department)
    
    def test_list_tas(self):
        response = self.client.get('/institutions/teaching-assistants/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['first_name'], 'Test')
        self.assertEqual(response.data[0]['last_name'], 'TA')
    
    def test_retrieve_ta(self):
        response = self.client.get(f'/institutions/teaching-assistants/{self.ta.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['first_name'], 'Test')
        self.assertEqual(response.data['last_name'], 'TA')
        self.assertEqual(response.data['department'], str(self.department.id))
        
# TODO: Implement UserEmailViewSetTest
# class UserEmailViewSetTest(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.institution = Institution.objects.create(name='Test Institution')
#         self.user_email = UserEmail.objects.create(name='Test@mail.com', institution=self.institution)
    
#     def test_list_user_emails(self):
#         response = self.client.get('/institutions/user-emails/')
#         self.assertEqual(response.status_code, 200)
