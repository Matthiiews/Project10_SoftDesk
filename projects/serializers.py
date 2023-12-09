from rest_framework import serializers

from projects.models import Project, Contributor, Issue, Comment


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for the Project model.
    This serializer includes all fields of the Project model and marks 
    'author' and 'id' as read-only.
    """
    class Meta:
        model = Project
        fields = '__all__'
        read_only__fields = ('author', 'id')


class ContributorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Contributor model.
    This serializer includes all fields of the Contributor model and marks 'project', 
    'role', and 'id' as read-only.
    """
    class Meta:
        model = Contributor
        fields = '__all__'
        read_only__fields = ('project', 'role', 'id')


class IssueSerializer(serializers.ModelSerializer):
    """
    Serializer for the Issue model.
    This serializer includes all fields of the Issue model and marks 'project', 
    'author', 'created_time', and 'id' as read-only.
    """
    class Meta:
        model = Issue
        fields = '__all__'
        read_only__fields = ('project', 'author', 'created_time', 'id')


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.
    This serializer includes all fields of the Comment model and marks 'author', 
    'issue', 'created_time', and 'id' as read-only.
    """
    class Meta:
        model = Comment
        fields = '__all__'
        read_only__fields = ('author', 'issue', 'created_time', 'id')
