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
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.course = Course.objects.create(
            full_name="Test Course",
            description="A test course for assignment completion.",
            privacy=False,
            course_number="1234",
            creator=self.user
        )
        self.client.login(username="testuser", password="testpassword")
        self.user.profile.courses.add(self.course)
        self.assignment = Assignment.objects.create(
            title="Test Assignment",
            description="This is a test assignment.",
            due_date="2024-12-15",
            user=self.user,
            course=self.course
        )

    def test_mark_assignment_as_completed(self):
        initial_response = self.client.get(reverse('assignments:assignment_list'))
        self.assertContains(initial_response, self.assignment.title)

        # Mark assignment as completed
        response = self.client.post(reverse('assignments:toggle_complete', args=[self.assignment.id]))
        self.assertEqual(response.status_code, 302)

        # Verify it is marked completed in the database
        self.assertTrue(self.user.profile.completed_assignments.filter(id=self.assignment.id).exists())

        # Check that it's no longer visible in the assignment list
        final_response = self.client.get(reverse('assignments:assignment_list'))

    def test_unmark_assignment_as_completed(self):
        # Pre-mark assignment as completed
        self.user.profile.completed_assignments.add(self.assignment)

        # Unmark assignment as completed
        response = self.client.post(reverse('assignments:toggle_complete', args=[self.assignment.id]))
        self.assertEqual(response.status_code, 302)

        # Verify it is not completed anymore
        self.assertNotIn(self.assignment, self.user.profile.completed_assignments.all())

        # Check "In Progress Assignments" section
        response = self.client.get(reverse('assignments:assignment_list'))
        self.assertContains(response, self.assignment.title)



@tag('file_search')
class FileSearchTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.course = Course.objects.create(
            full_name="Test Course",
            description="Test Description",
            privacy=False,
            course_number="1111",
            creator=self.user
        )
        self.user.profile.courses.add(self.course)
        
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

    def test_search_file_by_keyword(self):
        self.client.login(username="testuser", password="testpassword")
        
        # Search for keyword in assignment1
        response = self.client.get(reverse('assignments:file_search'), {'q': 'testing'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Assignment 1")
        self.assertNotContains(response, "Test Assignment 2")

        # Search for keyword in assignment2
        response = self.client.get(reverse('assignments:file_search'), {'q': 'example'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Assignment 2")
        self.assertNotContains(response, "Test Assignment 1")

        # Search for non-existent keyword
        response = self.client.get(reverse('assignments:file_search'), {'q': 'nonexistent'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No assignments found")

