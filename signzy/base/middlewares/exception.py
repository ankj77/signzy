import json
import logging
import traceback

from django import http
from django.shortcuts import render_to_response
from django.template import RequestContext

from apps.common.utils import Utils

logger = logging.getLogger(__name__)


class ExceptionMiddleWare(object):
    def process_exception(self, request, exception):
        logger.info("request.path " + request.path)
        logger.error("error: " + traceback.format_exc())

        # TODO: need a more elegant way to distinguish between json & html request
        urls = ['rest/v', 'discount']
        for url in urls:
            # json request
            if url in request.path:
                logger.info("json request")
                return self.handleException(request, exception)
        # request for an html page
        if isinstance(exception, http.Http404):
            return self.handle404(request, exception)
        else:
            return self.handle500(request, exception)

    def handle404(self, request, exception):
        logger.info('handle404 called')
        is_mobile = request.session.get('is_mobile')
        logger.debug('is_mobile in session: %s', is_mobile)
        if is_mobile:
            template = 'mobile/404.html'
        else:
            template = 'desktop/404.html'
        response = render_to_response(template, {}, context_instance=RequestContext(request))
        response.status_code = 404
        return response

    def handle500(self, request, exception):
        logger.info('handle500 called')
        is_mobile = request.session.get('is_mobile')
        logger.debug('is_mobile in session: %s', is_mobile)
        if is_mobile:
            template = 'mobile/500.html'
        else:
            template = 'desktop/500.html'
        response = render_to_response(template, {}, context_instance=RequestContext(request))
        response.status_code = 500
        return response

    def handleException(self, request, exception):
        if exception and hasattr(exception, 'code'):
            response = Utils.buildErrorResponseContext(exception.code)
        else:
            response = {'status': 'error', 'msg': 'Unknown Error', 'code': '101'}
        return http.HttpResponse(json.dumps(response))
