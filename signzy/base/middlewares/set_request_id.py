import threading
import uuid

thread_local = threading.local()


def get_current_user():
    return getattr(thread_local, 'user_id', None)


def get_current_request_id():
    return getattr(thread_local, 'request_id', None)


class RequestIDMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            thread_local.user_id = request.user.id
        else:
            thread_local.user_id = request.session.session_key
        thread_local.request_id = str(uuid.uuid4()).replace('-', '')

    def process_response(self, request, response):
        if hasattr(thread_local, 'user_id'):
            del thread_local.user_id
        if hasattr(thread_local, 'request_id'):
            del thread_local.request_id
        return response
