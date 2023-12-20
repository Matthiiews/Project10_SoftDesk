from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom user model with additional fields.
    This model extends the default Django `AbstractUser` model and includes
    additional fields for age, contact consent, and share consent.

    Attributes:
        age (PositiveSmallIntegerField): The user's age.
        can_be_contacted (BooleanField): Indicates whether the user can be
        contacted.
        can_data_be_shared (BooleanField): Indicates whether the user's data
        can be shared.
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
        String representation of the user.

        Returns:
            str: The username of the user.
        """
        return self.username
