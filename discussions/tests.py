from django.test import TestCase, tag
from django.contrib.auth.models import User
from discussions.models import Discussion, Comment
from courses.models import Course

class DiscussionBoardTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        # Create a test course
        self.course = Course.objects.create(
            full_name="Test Course",
            description="Test Description",
            privacy=False,
            course_number="1111",
            creator=self.user
        )

        # Ensure the user's profile has a courses relationship
        profile = self.user.profile
        profile.role = 'common_user'
        profile.save()
        profile.courses.add(self.course)

        # Create a test discussion
        self.discussion = Discussion.objects.create(
            title="Test Discussion",
            content="This is a test discussion content.",
            course=self.course,
            user=self.user
        )

    @tag("discussion_board")
    def test_post_comment(self):
        # Log in as the user
        self.client.login(username="testuser", password="testpassword")

        # Post a comment
        response = self.client.post(
            f'/discussions/{self.discussion.id}/', 
            {'content': "This is a test comment."}
        )

        # Debugging outputs
        print("User Courses:", self.user.profile.courses.all())
        print("Discussions:", Discussion.objects.all())
        print("Comments:", Comment.objects.all())
        print("Response Content:", response.content.decode())

        # Ensure the comment was successfully created
        self.assertEqual(response.status_code, 302) 
        self.assertEqual(self.discussion.comments.count(), 1)
        self.assertEqual(self.discussion.comments.first().content, "This is a test comment.")
        self.assertEqual(self.discussion.comments.first().user, self.user)
