from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User


class Contributor(models.Model):
    """
    Model representing a contributor to a project.
    Each contributor is associated with a user and a project.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)


class Project(models.Model):
    """
    Model representing a project.
    A project has a name, description, type (e.g., back-end, front-end),
    and creation time.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    type_choices = [
        ('back-end', 'Back-end'),
        ('front-end', 'Front-end'),
        ('iOS', 'iOS'), ('Android', 'Android')
    ]
    type = models.CharField(max_length=10, choices=type_choices)
    created_time = models.DateTimeField(auto_now=True)


class Issue(models.Model):
    """
    Model representing an issue in a project.
    An issue has a title, description, priority, tag, status, project association,
    and creation time.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    priority_choices = [('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High')]
    priority = models.CharField(max_length=6, choices=priority_choices)
    tag_choices = [('BUG', 'Bug'), ('FEATURE', 'Feature'), ('TASK', 'Task')]
    tag = models.CharField(max_length=8, choices=tag_choices)
    status_choices = [
        ('To Do', 'To Do'),
        ('In Progress', 'In Progress'),
        ('Finished', 'Finished')
    ]
    status = models.CharField(
        max_length=15, choices=status_choices, default='To Do')
    created_time = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    """Model representing a comment on an issue.
    A comment has an issue association, an author (user), text, 
    a unique identifier, and creation time.
    """
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    uuid = models.UUIDField(unique=True, default=uuid4, editable=False)
    created_time = models.DateTimeField(auto_now=True)


# Create your models here.
