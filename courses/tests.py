from django.test import TestCase, tag
from django.contrib.auth.models import User
from courses.models import Course
from django.urls import reverse

@tag('course_enrollment')
class CourseEnrollmentTest(TestCase):
    def setUp(self):
        # Create a test user to act as the creator
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Create some test courses
        self.course1 = Course.objects.create(
            full_name="Course 1",
            description="Description 1",
            privacy=False,
            course_number="1111",
            creator=self.user  # Assign the creator
        )
        self.course2 = Course.objects.create(
            full_name="Course 2",
            description="Description 2",
            privacy=True,
            course_number="2222",
            creator=self.user  # Assign the creator
        )

    def test_course_enrollment_moves_to_my_courses(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')
        
        # Enroll in the course
        response = self.client.post(reverse('courses:enroll_in_course', args=[self.course1.id]))
        self.assertEqual(response.status_code, 302)  # Ensure it redirects after enrollment

        # Verify the course is in "My Courses"
        self.assertIn(self.course1, self.user.profile.courses.all())

        # Verify it is no longer in the "Available Courses" section
        response = self.client.get(reverse('courses:course_list'))  # Replace with your actual course list URL
        self.assertNotContains(response, "Course 1")
        self.assertContains(response, "My Courses")

    def test_course_unenrollment_removes_from_my_courses(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')
        
        # Enroll in a course
        self.user.profile.courses.add(self.course1)

        # Unenroll from the course
        response = self.client.post(reverse('courses:unenroll_from_course', args=[self.course1.id]))
        self.assertEqual(response.status_code, 302)  # Ensure it redirects after unenrollment

        # Verify the course is no longer in "My Courses"
        self.assertNotIn(self.course1, self.user.profile.courses.all())
