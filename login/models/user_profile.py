from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from djutil.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _
from login import DefaultPermissions
from django.db import models


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel, DefaultPermissions):
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'),)
    MEMBER_TYPE = (('ALUMNI', 'Alumni'), ('STUDENT', 'Student'))

    first_name = models.CharField(_('First Name'), max_length=200)
    last_name = models.CharField(_('Last Name'), max_length=200, blank=True, default="")
    username = models.CharField(max_length=200, blank=True, default="")
    email = models.CharField(max_length=200)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    member_type = models.CharField(max_length=1, choices=MEMBER_TYPE)

    class Meta(DefaultPermissions.Meta):
        db_table = 'user_profile'
        verbose_name = _('user')
        verbose_name_plural = _('users')
