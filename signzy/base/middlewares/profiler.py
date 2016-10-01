from django.core.exceptions import MiddlewareNotUsed
from django.conf import settings
import cProfile
import pstats
import marshal
from cStringIO import StringIO

class ProfileMiddleware(object):
    """
    Usage:
        Pass 'profile' as query param to profile any view.
        Pass 'app_call' along with 'profile' to show results for only web application files
        Pass 'strip_dir' along with 'profile' to show just file name, instead of full directory structure.
        NOTE: 'strip_dir' will not work along with 'app_call'. Since 'app_call' filters based on presence of 'webapp' in file name, and 'strip_dir' will remove that.

    Generate in Graphical format:
        Install graphviz -
            sudo apt-get install graphviz, brew install graphviz
        pip install gprof2dot
        gprof2dot.py -f pstats output.pstats | dot -Tpng -o output.png
    """
    def __init__(self):
        if not settings.DEBUG:
            raise MiddlewareNotUsed()
        self.profiler = None

    def process_view(self, request, callback, callback_args, callback_kwargs):
        if settings.DEBUG and ('profile' in request.GET
                               or 'profilebin' in request.GET):
            self.profiler = cProfile.Profile()
            args = (request,) + callback_args
            return self.profiler.runcall(callback, *args, **callback_kwargs)

    def process_response(self, request, response):
        if settings.DEBUG:
            if 'profile' in request.GET:
                self.profiler.create_stats()
                out = StringIO()
                stats = pstats.Stats(self.profiler, stream=out)
                # Values for stats.sort_stats():
                # - calls           call count
                # - cumulative      cumulative time
                # - file            file name
                # - module          file name
                # - pcalls          primitive call count
                # - line            line number
                # - name            function name
                # - nfl                     name/file/line
                # - stdname         standard name
                # - time            internal time
                stats = stats.sort_stats(request.GET.get("sort", "time"))
                if "strip_dir" in request.GET:
                    stats.strip_dirs()
                if "app_call" in request.GET:
                    stats.sort_stats('cumulative').print_stats("webapp")
                else:
                    stats.sort_stats('cumulative').print_stats()
                response.content = out.getvalue()
                response['Content-type'] = 'text/plain'
            if 'profilebin' in request.GET:
                self.profiler.create_stats()
                response.content = marshal.dumps(self.profiler.stats)
                if "filename" in request.GET:
                    filename = request.GET.get("filename") + ".pstat"
                else:
                    filename = request.path.strip('/').replace('/','_') + '.pstat'
                response['Content-Disposition'] = \
                        'attachment; filename=%s' % (filename,)
                response['Content-type'] = 'application/octet-stream'
        return response
