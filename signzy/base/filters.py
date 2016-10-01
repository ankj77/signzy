import logging

import base.middlewares.set_request_id
from base.middlewares.set_request_id import get_current_user, get_current_request_id


class LogLevelFilter(logging.Filter):
    def __init__(self, level):
        self.level = level

    def filter(self, record):
        return record.levelno == self.level


class RequestIDFilter(logging.Filter):
    def filter(self, record):
        current_user = get_current_user()
        current_request_id = get_current_request_id()
        record.user_id = current_user
        record.request_id = current_request_id
        return True


class CeleryRequestIDFilter(logging.Filter):
    def __init__(self, user_id, request_id, task_id, task_name):
        self.user_id = user_id
        self.request_id = request_id
        self.task_id = task_id
        self.task_name = task_name
        base.middlewares.set_request_id.thread_local.user_id = self.user_id
        base.middlewares.set_request_id.thread_local.request_id = self.request_id

    def filter(self, record):
        record.user_id = self.user_id
        record.request_id = self.request_id
        record.task_id = self.task_id
        record.task_name = self.task_name
        return True
