import re


class ApiConstant(object):
    STATUS = "status"
    MESSAGE = "message"
    ERROR = "error"
    SUCCESS = "success"


class UtilsConstant(object):
    EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
