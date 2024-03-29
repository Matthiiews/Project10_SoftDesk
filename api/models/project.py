from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class Project(models.Model):
    """
    Modèle représentant un projet.
    Un projet a un nom, une description, un type (par exemple, back-end,
    front-end), et une heure de création.
    """
    # Types de projets
    BACKEND = "BKD"
    FRONTEND = "FTD"
    IOS = "IOS"
    ANDROID = "ARD"

    PROJECT_TYPES = [
        (BACKEND, "Back-end"),
        (FRONTEND, "Front-end"),
        (IOS, "iOS"),
        (ANDROID, "Android")
    ]

    created_time = models.DateField(
        auto_now_add=True, verbose_name=_("Created on"))
    name = models.CharField(max_length=100, verbose_name=_("Name of project"))
    description = models.TextField(verbose_name=_("Project description"))
    project_type = models.CharField(
        max_length=8, choices=PROJECT_TYPES, verbose_name=_("Project type")
    )
    author = models.ForeignKey(
        "api.User", on_delete=models.CASCADE, blank=True,
        related_name="Project_author", verbose_name=_("Project author")
    )
    contributors = models.ManyToManyField(
        "api.User", blank=True, related_name="Project_contributors",
        verbose_name=_("Project contributors")
    )

    def __str__(self) -> str:
        return f"{self.name} <{self.author}>"


class Issue(models.Model):
    """
    Modèle représentant un problème dans un projet.
    Un problème a un titre, une description, une priorité, un tag, un statut,
    une association au projet et une heure de création.
    Par défaut, l'état d'un problème est "À faire" (ToDo).
    """

    # Tags pour le problème
    BUG = "B"
    FEATURE = "FT"
    TASK = "TK"

    # États pour le problème
    TODO = "TD"
    IN_PROGRESS = "IP"
    FINISHED = "FS"

    # Priorité pour le problème
    LOW = "L"
    MEDIUM = "M"
    HIGH = "H"

    TAGS = [
        (BUG, "Bug"),
        (FEATURE, "Feature"),
        (TASK, "Task"),
    ]

    STATE = [
        (TODO, "ToDo"),
        (IN_PROGRESS, "In Progress"),
        (FINISHED, "Finished"),
    ]

    PRIORITY = [
        (LOW, "Low"),
        (MEDIUM, "Medium"),
        (HIGH, "High"),
    ]

    created_time = models.DateTimeField(
        auto_now_add=True, verbose_name=_("created on"))
    author = models.ForeignKey("api.User", on_delete=models.CASCADE,
                               related_name="issue_authors", blank=True,
                               verbose_name=_("Issue Author"))
    assigned_to = models.ForeignKey("api.User", on_delete=models.CASCADE,
                                    related_name="Issue_contributors",
                                    verbose_name=_("Issue assigned to"))
    name = models.CharField(
            max_length=100, verbose_name=_("Name of issue"),
    )
    description = models.TextField(verbose_name=_("Issue description"))
    tag = models.CharField(
            max_length=4, choices=TAGS, verbose_name=_("Issue tag"),
    )
    state = models.CharField(
            max_length=4, choices=STATE, default=TODO,
            verbose_name=_("Issue state"),
    )
    priority = models.CharField(
            max_length=1, choices=PRIORITY, verbose_name=_("Issue priority"),
    )
    project = models.ForeignKey(
            "api.Project", on_delete=models.CASCADE, related_name="Issues",
            verbose_name=_("Related project"),
    )

    def __str__(self):
        return (f"{self.name} | {self.tag} | {self.state} | {self.priority} | {self.project} ")


class Comment(models.Model):
    """
    Un commentaire est lié à un problème
    """

    created_time = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Created on"),
    )
    author = models.ForeignKey("api.User", on_delete=models.CASCADE,
                               blank=True, related_name="comment_authors",
                               verbose_name=_("Comment author"))
    name = models.CharField(max_length=100, verbose_name=_("Comment name"))
    description = models.TextField(verbose_name=_("Comment body"))
    issue = models.ForeignKey("api.Issue", on_delete=models.CASCADE,
                              blank=True, related_name="comments",
                              verbose_name=_("Related issue"))
    issue_url = models.URLField(
        blank=True, verbose_name=_("Url verse an issue"))
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return f"{self.name} | {self.issue}"
