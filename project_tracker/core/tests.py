from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from .models import StudentProfile, FacultyProfile, Project


class StudentProfileTestCase(TestCase):
    """Test cases for StudentProfile model"""

    def setUp(self):
        """Create test data"""
        self.user = User.objects.create_user(username='teststudent', password='testpass123')
        self.student_group, _ = Group.objects.get_or_create(name='Student')
        self.user.groups.add(self.student_group)

    def test_student_profile_creation(self):
        """Test creating a StudentProfile"""
        profile = StudentProfile.objects.create(
            user=self.user,
            register_number='CS001',
            department='Computer Science',
            year=3
        )
        self.assertEqual(profile.register_number, 'CS001')
        self.assertEqual(profile.department, 'Computer Science')


class FacultyProfileTestCase(TestCase):
    """Test cases for FacultyProfile model"""

    def setUp(self):
        """Create test data"""
        self.user = User.objects.create_user(username='testfaculty', password='testpass123')
        self.faculty_group, _ = Group.objects.get_or_create(name='Faculty')
        self.user.groups.add(self.faculty_group)

    def test_faculty_profile_creation(self):
        """Test creating a FacultyProfile"""
        profile = FacultyProfile.objects.create(
            user=self.user,
            employee_id='FAC001',
            department='Computer Science',
            designation='Assistant Professor'
        )
        self.assertEqual(profile.employee_id, 'FAC001')
        self.assertEqual(profile.designation, 'Assistant Professor')


class CoreModelsAndViewsTest(TestCase):
    def setUp(self):
        # create groups
        self.student_group, _ = Group.objects.get_or_create(name='Student')
        self.faculty_group, _ = Group.objects.get_or_create(name='Faculty')

        # create a student user
        self.student_user = User.objects.create_user(username='stud1', password='pass')
        self.student_user.groups.add(self.student_group)
        self.student_profile = StudentProfile.objects.create(user=self.student_user, register_number='REG123', department='CSE', year=4)

        # create a faculty user
        self.faculty_user = User.objects.create_user(username='fac1', password='pass')
        self.faculty_user.groups.add(self.faculty_group)
        self.faculty_profile = FacultyProfile.objects.create(user=self.faculty_user, employee_id='EMP1', department='CSE', designation='Professor')

        self.client = Client()

    def test_student_project_submission_view(self):
        self.client.login(username='stud1', password='pass')
        resp = self.client.get('/student/dashboard/')
        self.assertEqual(resp.status_code, 200)

        # submit a project with valid data (description must be 10+ chars)
        resp = self.client.post('/student/dashboard/', {'title': 'Test Project', 'domain': 'AI', 'description': 'This is a detailed project description'})
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Project.objects.filter(title='Test Project').exists())

    def test_faculty_review_and_report_generation(self):
        # create a project first
        project = Project.objects.create(student=self.student_profile, title='P2', domain='ML', description='D')
        self.client.login(username='fac1', password='pass')
        resp = self.client.get('/faculty/dashboard/')
        self.assertEqual(resp.status_code, 200)

        # review project
        resp = self.client.post('/faculty/dashboard/', {'project_id': project.id, 'status': Project.STATUS_APPROVED, 'faculty_remarks': 'Good'})
        self.assertEqual(resp.status_code, 302)
