from django.test import TestCase, tag
from django.contrib.auth.models import User
from assignments.models import Assignment, AssignmentFile
from courses.models import Course

@tag('file_search')
class FileSearchTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a test course
        self.course = Course.objects.create(
            full_name="Test Course",
            description="Test Description",
            privacy=False,
            course_number="1111",
            creator=self.user
        )

        # Create assignments
        self.assignment1 = Assignment.objects.create(
            title="Test Assignment 1",
            description="Description 1",
            due_date="2024-12-10",
            course=self.course,
            user=self.user,
            keywords="testing, search"
        )

        self.assignment2 = Assignment.objects.create(
            title="Test Assignment 2",
            description="Description 2",
            due_date="2024-12-15",
            course=self.course,
            user=self.user,
            keywords="filtering, example"
        )

        # Attach files to assignments
        AssignmentFile.objects.create(
            assignment=self.assignment1,
            file="files/test1.pdf",
            title="Test File 1",
            description="A file for testing keyword search"
        )

        AssignmentFile.objects.create(
            assignment=self.assignment2,
            file="files/test2.pdf",
            title="Test File 2",
            description="Another file for testing"
        )

    def test_search_file_by_keyword(self):
        # Log in as the user
        self.client.login(username="testuser", password="testpassword")

        # Test searching for a keyword present in assignment1
        response = self.client.get('/file_search/', {'q': 'testing'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Assignment 1")
        self.assertNotContains(response, "Test Assignment 2")
