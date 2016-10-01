from django.contrib.auth.models import AbstractBaseUser, User
from djutil.models import TimeStampedModel
from django.db import models

from signzy.apps.login.model_helpers import user_manager
from signzy.apps.login.models.permissions import DefaultPermissions, PermissionsMixin
from django.utils.translation import ugettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel, DefaultPermissions):
    MALE = 'Male'
    FEMALE = 'Female'
    ALUMNI = 'Alumni'
    STUDENT = 'Student'
    GENDER_CHOICES = ((MALE, MALE), (FEMALE, FEMALE))
    MEMBER_TYPE = ((ALUMNI, ALUMNI), (STUDENT, STUDENT))
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, blank=True, default="")
    username = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.CharField(max_length=200, unique=True)
    gender = models.CharField(max_length=30, choices=GENDER_CHOICES, default=MALE)
    member_type = models.CharField(max_length=40, choices=MEMBER_TYPE, default=ALUMNI)
    is_active = models.BooleanField(_('active'), default=False)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_verified = models.BooleanField(default=False)
    objects = user_manager.CustomUserManager()
    USERNAME_FIELD = 'email'

    class Meta(DefaultPermissions.Meta):
        db_table = 'profiles'
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return "%s(%s)" % (self.email, self.username)

    @staticmethod
    def authenticate(email=None, username=None, password=None):  # Check the username/password and return a User.
        if username != None and password != None:
            # Get the user
            try:
                user = User.objects.get(username=username)
                if user.check_password(password):
                    # logger.info('User is authenticated, logging user in')
                    return user
            except User.DoesNotExist:
                pass
        elif email != None and password != None:
            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    # logger.info('User is authenticated, logging user in')
                    return user
            except User.DoesNotExist:
                pass
        return None
