import re


class API(object):
    STATUS = "status"
    MESSAGE = "message"
    ERROR = "error"
    SUCCESS = "success"
    PAYLOAD = "payload"


class UtilsConstant(object):
    EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
