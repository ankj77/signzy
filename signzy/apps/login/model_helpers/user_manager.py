# -*- coding: utf-8 -*-

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager
from django.utils.crypto import get_random_string


class CustomUserManager(UserManager):
    def _create_user(self, email, username, password, is_staff, is_superuser, is_active, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, is_staff=is_staff, is_superuser=is_superuser,
                          is_active=is_active, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, username=None, **kwargs):
        return self.create_user(email=email, username=None, password=password, is_staff=True, is_superuser=True,
                                is_active=True,
                                **kwargs)

    def create_user(self, email, username=None, password=None, is_staff=False, is_superuser=False, is_active=True,
                    **kwargs):
        return self._create_user(email, username, password, is_staff, is_superuser, is_active, **kwargs)

    def create_unconfirmed_user(self, email=None, password=None, account_type=None, **extra_fields):

        if password is None:
            password = make_password(None)
        return super(CustomUserManager, self).create_user(
            email, password, account_type=account_type,
            is_active=False, **extra_fields
        )

    def generate_random_username(self):
        """
        Usernames that start with '!' are generated randomly and
        cannot be used for login until changed by the user.
        """
        return "!{}".format(get_random_string(length=16))
