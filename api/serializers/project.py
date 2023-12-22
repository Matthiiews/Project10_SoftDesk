from rest_framework import serializers

from api.models.project import Project, Issue, Comment


class ProjectCreateSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour créer un projet
    - Le nom, la description et le type de projet sont obligatoires
    """

    class Meta:
        model = Project
        fields = ["id", "name", "description", "project_type"]

    def validate(self, attrs):
        if (self.context["view"]
            .project.filter(name=attrs["name"],
                            project_type=attrs["project_type"]).exists()):
            raise serializers.ValidationError(
                "Attention! This project exists already.")
        return attrs


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name", "author", "contributors",]


class ProjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id", "created_time", "name", "description",
                  "project_type", "author", "contributors",
        ]


class IssueCreateSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour créer un problème
    - Champs obligatoires : nom, description, état, tag, priorité et
    attribué à
    """

    class Meta:
        models = Issue
        fields = [
            "id", "assigned_to", "name", "description",
            "tag", "state", "priority"
        ]

    def validate(self, attrs):
        if (
            self.context["view"].issue.filter(
                name=attrs["name"], tag=attrs["tag"], state=attrs["state"],
                priority=attrs["priority"],
            )
            .exists()
        ):
            raise serializers.ValidationError("This issue exists already!")
        return attrs


class IssueListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            "id", "author", "assigned_to", "name", "description",
            "tag", "state", "priority", "project",
        ]


class IssueDetailSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            "id", "created_time", "author", "assigned_to", "name",
            "description", "tag", "state", "priority", "project",
        ]


class CommentCreateSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour créer un commentaire
    - Champs obligatoires : nom et description.
    """

    class Meta:
        model = Comment
        fields = ["id", "comment", "description"]

    def validate(self, value):
        if self.context["view"].comment.filter(name=value).exists():
            raise serializers.ValidationError(
                "This comment name exists already.")
        return value


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "author", "name", "issue"]


class CommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id", "uuid", "created_time", "author", "name",
            "description", "issue", "issue_url",
        ]
