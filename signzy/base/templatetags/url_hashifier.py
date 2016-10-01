import json
import logging
import re
import os
from django import template
from django.conf import settings


register = template.Library()
logger = logging.getLogger(__name__)

# variables
env = getattr(settings, "ENVIRONMENT", None)
mapperFileName = 'mapper.json'
webAppName = 'webapp'
webapp_path = os.path.abspath(os.path.dirname(__name__)) + '/' + webAppName + '/dist/'
desktop_mapper = None
mobile_mapper = None
try:
    with open(webapp_path + 'desktop/' + mapperFileName) as file:
        desktop_mapper = json.load(file)
except:
    logger.exception("mapper.json is not present at :%s", (webapp_path + 'desktop/'));

try:
    with open(webapp_path + 'mobile/' + mapperFileName) as file:
        mobile_mapper = json.load(file)
except:
    logger.exception("mapper.json is not present at :%s", (webapp_path + 'mobile/'));

'''
    Registers a filter to be used for getting hashified url from a normal url

    Usage pattern -
    'desktop/js/abc.js'|hashify:'desktop'
    output from dist/desktop/mapper.json => 'desktop/js/abc-f4nb2snu3yxs88.min.js

    It can be used anywhere in templates
'''

@register.filter
def hashify(url, args='desktop'):
    if env == 'local':
        return url
    url = re.sub(r"([^/]*/){2}", "", url)
    if args == 'desktop':
        mapper = desktop_mapper
    else:
        mapper = mobile_mapper

    if mapper is None:
        return args + '/' + url
    if url not in mapper:
        return args + '/' + url

    return args + '/' + mapper[url]
