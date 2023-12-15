from rest_framework import permissions
from rest_framework.generics import get_object_or_404

from .models import Project, Issue, Comment


class ProjectPermissions(permissions.BasePermission):
    """
    Custom permissions for Project-related views.
    This permission class checks whether the requesting user has permission
    to perform the requested action on a Project instance.
    """
    def has_permission(self, request, view):
        try:
            project = get_object_or_404(Project, id=view.kwargs['project_pk'])

            # Allow safe methods (GET, HEAD, OPTIONS) for contributors
            if request.method in permissions.SAFE_METHODS:
                return project in Project.objects.filter(
                    contributors_user=request.user)

            # Allow modification only by the project's author
            return request.user == project.author

        except KeyError:
            # If project ID is not provided, allow the action
            return True


class ContributorPermissions(permissions.BasePermission):
    """
    Custom permissions for Contributor-related views.
    This permission class checks whether the requesting user has permission to
    perform the requested action on a Contributor instance.
    """
    def has_permission(self, request, view):
        project = get_object_or_404(Project, id=view.kwargs['project_pk'])

        # Allow safe methods (GET, HEAD, OPTIONS) for contributors
        if request.method in permissions.SAFE_METHODS:
            return project in Project.objects.filter(
                contributors__user=request.user)

        # Allow modification only by the project's author
        return request.user == project.author


class IssuePermissions(permissions.BasePermission):
    """
    Custom permissions for Issue-related views.
    This permission class checks whether the requesting user has permission to
    perform the requested action on an Issue instance.
    """
    def has_permission(self, request, view):
        project = get_object_or_404(Project, id=view.kwargs['project_pk'])
        try:
            issue = get_object_or_404(Issue, id=view.kwargs['issue_pk'])
            # Allow modification only by the issue's author
            return request.user == issue.author
        except KeyError:
            # If issue ID is not provided, allow the action if the user is a
            # contributor
            return project in Project.objects.filter(
                contributors__user=request.user)


class CommentPermissions(permissions.BasePermission):
    """
    Custom permissions for Comment-related views.
    This permission class checks whether the requesting user has permission to
    perform the requested action on a Comment instance.
    """
    def has_permission(self, request, view):
        project = get_object_or_404(Project, id=view.kwargs['project_pk'])
        try:
            comment = get_object_or_404(Comment, id=view.kwargs['comment_pk'])
            # Allow safe methods (GET, HEAD, OPTIONS) for contributors
            if request.method in permissions.SAFE_METHODS:
                return project in Project.objects.filter(
                    contributors__user=request.user)

            # Allow modification only by the comment's author
            return request.user == comment.author
        except KeyError:
            # If comment ID is not provided, allow the action if the user is a
            # contributor
            return project in Project.objects.filter(
                contributors__user=request.user)
