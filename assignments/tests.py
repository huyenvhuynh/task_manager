from django.test import TestCase, tag
from django.contrib.auth.models import User
from courses.models import Course
from assignments.models import Assignment
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

        # Assign the user to the course
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

        # Ensure both assignments are displayed
        self.assertContains(response, "Assignment 1")
        self.assertContains(response, "Assignment 2")

        # Ensure both due dates are included in the JSON assignments data
        self.assertContains(response, '"due_date": "2024-12-15"')
        self.assertContains(response, '"due_date": "2024-12-20"')
