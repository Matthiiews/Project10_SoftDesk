from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Modèle d'utilisateur personnalisé avec des champs supplémentaires.
    Ce modèle étend le modèle par défaut d'utilisateur de Django,
    `AbstractUser`, et inclut des champs supplémentaires pour l'âge,
    le consentement de contact et le consentement de partage.

    Attributs:
        age (PositiveSmallIntegerField): L'âge de l'utilisateur.
        peut_etre_contacte (BooleanField): Indique si l'utilisateur peut être
        contacté.
        peut_partager_donnees (BooleanField): Indique si les données de
        l'utilisateur peuvent être partagées.
    """
    age = models.PositiveSmallIntegerField(
        default=15, validators=[MinValueValidator(15)], verbose_name=_("Age"),
        help_text=_("User's age."))
    can_be_contacted = models.BooleanField(
        verbose_name=("Contact Consent"), default=False,
        help_text=_("Indicates whether the user can be contacted."))
    can_data_be_shared = models.BooleanField(
        verbose_name=("Share Consent"), default=False,
        help_text=_("Indicates whether the user's data can be shared."))

    def __str__(self) -> str:
        """
        Représentation sous forme de chaîne de caractères de l'utilisateur.

        Returns:
            str: Le nom d'utilisateur de l'utilisateur.
        """
        return self.username
