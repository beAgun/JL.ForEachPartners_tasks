from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, Group, Permission, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class MyUserManager(UserManager):

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """

        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        # username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def get_by_natural_key(self, email):
        return self.get(**{self.model.EMAIL_FIELD: email})


class User(AbstractUser):

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[AbstractUser.username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
        # default=''
    )

    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    # USERNAME_FIELD = 'username'

    objects = MyUserManager()

    def __str__(self):
        return f'{self.username}'