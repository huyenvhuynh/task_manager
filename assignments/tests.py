from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from .models import Assignment, Course
import os

# Create your tests here.

# This tests the GitHub issue 'List View #6', 'Add Assignment #8'
class AssignmentTests(TestCase):
    def setUp(self):
        # Create a user and log in
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='password',
            email='testuser@example.com'
        )
        self.client.login(username='testuser', password='password')
        self.course = Course.objects.create(course_number=2130, course_name='CSO1')
        
        # # Define a valid file for upload
        # self.valid_file = SimpleUploadedFile(
        #     "file.txt",
        #     b"file content",
        #     content_type="text/plain"
        # )
        # self.invalid_file = SimpleUploadedFile(
        #     "file.exe",
        #     b"invalid content",
        #     content_type="application/octet-stream"
        # )
        

    # def test_add_assignment_get_request(self):
    #     # Testing GET reqeust to add_assignment redirects to home
    #     response = self.client.get(reverse('myapp:add_assignment'))
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, reverse('myapp:home'))

    # def test_add_assignment_post_valid(self):
    #     # Testing POST request to add_assignment with valid data and file.
    #     response = self.client.post(
    #         reverse('myapp:add_assignment'),
    #         {
    #             'title': 'Test Assignment',
    #             'description': 'This is a test assignment.',
    #             'due_date': '2024-12-31',
    #             'file_upload': self.valid_file
    #         }
    #     )
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, reverse('myapp:assignment_list'))
    #     self.assertEqual(Assignment.objects.count(), 1)
    #     assignment = Assignment.objects.first()
    #     self.assertEqual(assignment.title, 'Test Assignment')
    #     self.assertEqual(assignment.user, self.user)

    # def test_add_assignment_post_invalid_file(self):
    #     # Testing POST request to add_assignment with an invalid file type.
    #     response = self.client.post(
    #         reverse('myapp:add_assignment'),
    #         {
    #             'title': 'Test Assignment with Invalid File',
    #             'description': 'This assignment has an invalid file.',
    #             'due_date': '2024-12-31',
    #             'file_upload': self.invalid_file
    #         }
    #     )
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(response.content.decode(), 'Invalid file type.')
    #     self.assertEqual(Assignment.objects.count(), 0)

    # def test_assignment_list(self):
    #     # Testing that assignment_list view returns assignments for the logged-in user.
        
    #     Assignment.objects.create(
    #         title='Existing Assignment',
    #         description='This is an existing assignment.',
    #         due_date='2024-12-31',
    #         user=self.user,
    #         course=self.course
    #     )
    #     response = self.client.get(reverse('myapp:assignment_list'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'myapp/assignment_list.html')
    #     self.assertContains(response, 'Existing Assignment')

    # def test_delete_assignment(self):
    #     # Testing that delete_assignment removes an assignment.
        
    #     assignment = Assignment.objects.create(
    #         title='Assignment to Delete',
    #         description='This assignment will be deleted.',
    #         due_date='2024-12-31',
    #         user=self.user,
    #         course=self.course
    #     )
    #     response = self.client.post(reverse('myapp:delete_assignment', args=[assignment.id]))
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, reverse('myapp:assignment_list'))
    #     self.assertEqual(Assignment.objects.count(), 0)

    # def test_home_view_redirect_when_not_logged_in(self):
    #     self.client.logout()
    #     response = self.client.get(reverse('assignments:home'))
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, reverse('users:sign_in'))

    # def test_create_basic_assignment(self):
    #     assignment = Assignment.objects.create(
    #         title='Test Assignment',
    #         description='Test Description',
    #         due_date='2024-12-31',
    #         user=self.user,
    #         course=self.course
    #     )
    #     self.assertEqual(Assignment.objects.count(), 1)
    #     self.assertEqual(assignment.title, 'Test Assignment')
    #     self.assertEqual(assignment.course, self.course)

