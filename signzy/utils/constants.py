import re


class UserConstant(object):
    LOGIN_SUCCESS = "LOGIN_SUCCESS"
    LOGIN_FAILED = "LOGIN_FAILED"
    SIGNUP_SUCCESS = "SIGNUP_SUCCESS"
    SIGNUP_FAILED = "SIGNUP_FAILED"
    USERNAME_ALREADY_PRESENT = "USERNAME_ALREADY_PRESENT"
    USER_ALREADY_PRESENT = "USER_ALREADY_PRESENT"
    USER_NOT_FOUND = "USER_NOT_FOUND"
    USER_PASSWORD_MISMATCH = "USER_PASSWORD_MISMATCH"


class ApiConstant(object):
    STATUS = "status"
    MESSAGE = "message"
    ERROR = "error"
    SUCCESS = "success"


class UtilsConstant(object):
    EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
