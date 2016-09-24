from django.db import models
from django.utils.translation import ugettext_lazy as _


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    modified_at = models.DateTimeField(_("Modified at"), auto_now=True)

    class Meta:
        abstract = True


class DefaultPermissions(models.Model):
    class Meta:
        abstract = True
        default_permissions = ('add', 'change', 'delete', 'read')
