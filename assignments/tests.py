from django.test import TestCase, tag
from django.contrib.auth.models import User
from courses.models import Course
from assignments.models import Assignment, AssignmentFile
from django.urls import reverse

@tag('calendar_view')
class CalendarViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        # Create a test course
        self.course = Course.objects.create(
            full_name="Test Course",
            description="A test course for calendar testing.",
            privacy=False,
            course_number="1234",
            creator=self.user
        )

        # Log in the test user
        self.client.login(username="testuser", password="testpassword")

        self.user.profile.courses.add(self.course)

    def test_new_assignment_appears_on_calendar(self):
        # Create a new assignment for the test course
        assignment = Assignment.objects.create(
            title="Test Assignment",
            description="This is a test assignment.",
            due_date="2024-12-15",
            user=self.user,
            course=self.course
        )

        # Access the calendar view
        response = self.client.get(reverse('assignments:calendar'))

        # Ensure the request is successful
        self.assertEqual(response.status_code, 200)

        # Check if the assignment's title is present in the rendered calendar
        self.assertContains(response, "Test Assignment")

        # Check if the assignment's due date is included in the JSON assignments data
        self.assertContains(response, '"due_date": "2024-12-15"')

    def test_multiple_assignments_displayed_correctly(self):
        # Create multiple assignments
        Assignment.objects.create(
            title="Assignment 1",
            description="Description 1",
            due_date="2024-12-15",
            user=self.user,
            course=self.course
        )
        Assignment.objects.create(
            title="Assignment 2",
            description="Description 2",
            due_date="2024-12-20",
            user=self.user,
            course=self.course
        )

        # Access the calendar view
        response = self.client.get(reverse('assignments:calendar'))

        self.assertContains(response, "Assignment 1")
        self.assertContains(response, "Assignment 2")

        self.assertContains(response, '"due_date": "2024-12-15"')
        self.assertContains(response, '"due_date": "2024-12-20"')


@tag('assignment_completion')
class AssignmentCompletionTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        # Create a test course
        self.course = Course.objects.create(
            full_name="Test Course",
            description="A test course for assignment completion.",
            privacy=False,
            course_number="1234",
            creator=self.user
        )

        # Log in the test user
        self.client.login(username="testuser", password="testpassword")

        # Assign the user to the course
        self.user.profile.courses.add(self.course)

        # Create a test assignment
        self.assignment = Assignment.objects.create(
            title="Test Assignment",
            description="This is a test assignment.",
            due_date="2024-12-15",
            user=self.user,
            course=self.course
        )

    def test_mark_assignment_as_completed(self):
        # Mark the assignment as completed
        response = self.client.post(reverse('assignments:toggle_complete', args=[self.assignment.id]))

        self.assertEqual(response.status_code, 302)

        # Check that the assignment is now in the "Completed Assignments" section
        self.assertIn(self.assignment, self.user.profile.completed_assignments.all())

        # Access the assignment list view
        response = self.client.get(reverse('assignments:assignment_list'))

        # Ensure the completed assignment is not in the "In Progress Assignments" section
        self.assertNotContains(response, '<h3>In Progress Assignments</h3>')
        self.assertNotContains(response, 'Test Assignment', html=True)

        self.assertContains(response, '<h3>Completed Assignments</h3>', html=True)
        self.assertContains(response, 'Test Assignment')

    def test_unmark_assignment_as_completed(self):
        # Mark the assignment as completed
        self.user.profile.completed_assignments.add(self.assignment)

        # Unmark the assignment as completed
        response = self.client.post(reverse('assignments:toggle_complete', args=[self.assignment.id]))

        self.assertEqual(response.status_code, 302)

        # Check that the assignment is no longer in the "Completed Assignments" section
        self.assertNotIn(self.assignment, self.user.profile.completed_assignments.all())

        response = self.client.get(reverse('assignments:assignment_list'))

        self.assertContains(response, '<h3>In Progress Assignments</h3>', html=True)
        self.assertContains(response, 'Test Assignment')
        self.assertNotContains(response, '<h3>Completed Assignments</h3>')


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
        response = self.client.get(reverse('assignments:file_search'), {'q': 'testing'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Assignment 1")
        self.assertNotContains(response, "Test Assignment 2")

        # Test searching for a keyword present in assignment2
        response = self.client.get(reverse('assignments:file_search'), {'q': 'example'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Assignment 2")
        self.assertNotContains(response, "Test Assignment 1")

        # Test searching for a keyword not present
        response = self.client.get(reverse('assignments:file_search'), {'q': 'nonexistent'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No assignments found.")
