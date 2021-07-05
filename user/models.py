from django.contrib.auth.models import AbstractUser, Group
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

# Create your models here.
class MyUser(AbstractUser):
    # Some rules adding username
    username_validator = UnicodeUsernameValidator()

    #Custom Field
    email = models.EmailField(_('email'), max_length=80, unique=True)
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
        blank=True # Same code that has django as a default only added this to say can be an empty value
    )
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)

    # Field for login
    USERNAME_FIELD = 'email'

    # Field for command createsuperuser
    REQUIRED_FIELDS = ['username','first_name','last_name']

    def __str__(self):
        return f"{self.email}"