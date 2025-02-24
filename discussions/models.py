from django.db import models
from django.contrib.auth.models import User
from courses.models import Course

class Discussion(models.Model):
    """
    Model representing a discussion thread within a course.

    Attributes:
        title (CharField): The title of the discussion.
        content (TextField): The content/body of the discussion.
        course (ForeignKey): The course to which this discussion belongs.
        user (ForeignKey): The user who created the discussion.
        created_at (DateTimeField): The timestamp when the discussion was created.
        updated_at (DateTimeField): The timestamp when the discussion was last updated.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name='discussions'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']  # Orders discussions by most recent creation date by default.

    def __str__(self):
        """
        Returns:
            str: The string representation of the discussion, which is its title.
        """
        return self.title

class Comment(models.Model):
    """
    Model representing a comment within a discussion.

    Attributes:
        discussion (ForeignKey): The discussion to which this comment belongs.
        user (ForeignKey): The user who posted the comment.
        content (TextField): The content of the comment.
        created_at (DateTimeField): The timestamp when the comment was created.
        updated_at (DateTimeField): The timestamp when the comment was last updated.
    """
    discussion = models.ForeignKey(
        Discussion, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']  # Orders comments by creation date, oldest first.

    def __str__(self):
        """
        Returns:
            str: A formatted string representation of the comment, showing the user and discussion title.
        """
        return f'Comment by {self.user.username} on {self.discussion.title}'
