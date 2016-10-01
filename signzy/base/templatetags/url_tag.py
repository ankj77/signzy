from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def get_image_url():
    # S3_URL = 'https://%s.s3.amazonaws.com/' % settings.AWS_STORAGE_BUCKET_NAME
    S3_URL = settings.S3_URL
    return S3_URL


@register.simple_tag
def get_static_url():
    STATIC_URL = settings.STATIC_URL
    return STATIC_URL
