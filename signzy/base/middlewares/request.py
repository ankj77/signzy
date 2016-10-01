import json
import logging
import urlparse

from django.http.response import HttpResponseRedirect

logger = logging.getLogger(__name__)


class RequestMiddleWare(object):
    def process_request(self, request):

        # IE support page for IE browser
        if 'HTTP_USER_AGENT' in request.META:
            user_agent = request.META['HTTP_USER_AGENT'].lower()
            if ('msie' in user_agent or 'trident' in user_agent) and 'iesupport' in request.path:
                pass
            elif 'msie' in user_agent or 'trident' in user_agent:
                return HttpResponseRedirect('/iesupport')

        if len(request.GET):
            logger.info('GET params ' + json.dumps(request.GET))
        elif len(request.POST):
            logger.info('POST params ' + json.dumps(request.POST))

        # setattr(request, 'is_mobile', 1)

        # associate request with a session if unavailable
        if not request.session.session_key:
            request.session.save()

        ########################################
        # Add utm_parameters to session object #
        ########################################

        if request.user and request.user.is_active and request.user.is_authenticated():
            request.session['isAuthenticated'] = True
        else:
            request.session['isAuthenticated'] = False

        request_full_path = request.get_full_path()
        parameters_list = urlparse.urlparse(request_full_path)
        utm_source = urlparse.parse_qs(parameters_list.query).get('utm_source', None)
        utm_medium = urlparse.parse_qs(parameters_list.query).get('utm_medium', None)
        utm_campaign = urlparse.parse_qs(parameters_list.query).get('utm_campaign', None)
        utm_term = urlparse.parse_qs(parameters_list.query).get('utm_term', None)
        utm_content = urlparse.parse_qs(parameters_list.query).get('utm_content', None)

        if any([utm_source, utm_medium, utm_campaign, utm_term, utm_content]):
            if request.session != None:
                request.session['utm_params'] = {
                    "source": utm_source[0] if utm_source is not None else "",
                    "medium": utm_medium[0] if utm_medium is not None else "",
                    "name": utm_campaign[0] if utm_campaign is not None else "",
                    "term": utm_term[0] if utm_term is not None else "",
                    "content": utm_content[0] if utm_content is not None else ""
                }


                # TODO: attach a unique request id if one doesnt exist already in the request
                # TODO: identify if this is a mobile site call
