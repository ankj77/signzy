import functools
import logging
import traceback
from django.http import HttpRequest
from rest_framework.request import Request

LOG = logging.getLogger(__name__)


# Should not be used on @staticmethod or @classmethod. This will fail.
def log_args(logger=None, only_on_exception=False):
    def decorator(func):
        try:
            argnames = func.func_code.co_varnames[:func.func_code.co_argcount]
        except:
            argnames = None
        try:
            fname = func.func_name
        except:
            fname = None

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            argument_list = []
            if argnames:
                for entry in zip(argnames, args):
                    name = entry[0]
                    value = entry[1]
                    if name == 'request':
                        if isinstance(value, HttpRequest):
                            if value.method == 'GET':
                                name = 'TemplateView request.GET'
                                value = value.GET
                            elif value.method == 'POST':
                                name = 'TemplateView request.POST'
                                value = value.POST
                        elif isinstance(value, Request):
                            if value.method == 'GET':
                                name = 'APIView request.GET'
                                value = value.GET
                            else:
                                name = 'APIView request.data'
                                value = value.data
                    argument_list.append('{0}={1}'.format(name, value))
            else:
                for arg in args:
                    argument_list.append('{0}'.format(arg))

            for entry in kwargs.items():
                argument_list.append('{0}={1}'.format(entry[0], entry[1]))

            argument_values = ', '.join(argument_list)
            log = logger if logger else LOG
            if not only_on_exception:
                log.info("Function:[%s] called with args: %s", fname, argument_values)
            try:
                return func(*args, **kwargs)
            except:
                if only_on_exception:
                    log.error(traceback.format_exc())
                    log.exception("Function:[%s] called with args: %s", fname, argument_values)
                raise
        return wrapper

    return decorator
