import urlparse

from django.conf import settings


class ResponseMiddleWare(object):
    def process_response(self, request, response):
        if response.status_code not in settings.SERVER_STATUS_CAPTURE_FILTER:
            event_args = {
                "status_code": response.status_code,
                "origin_url": request.path,
                "request_method": request.method,
                "http_referrer": request.META.get('HTTP_REFERER'),
                "http_user_agent": request.META.get('HTTP_USER_AGENT'),
                "client_ip": request.META.get('REMOTE_ADDR'),
                "ajax_call": request.is_ajax()
            }
            # commonUtils.captureAnalyticsServerErrors(request,'Response Error',event_args)

        ''' This code is for conditional pixel
            Setting utm_source and utm_medium in cookies if they are present in url '''
        request_full_path = request.get_full_path()
        parameters_list = urlparse.urlparse(request_full_path)
        utm_campaign = urlparse.parse_qs(parameters_list.query).get('utm_campaign', None)
        utm_source = urlparse.parse_qs(parameters_list.query).get('utm_source', None)
        utm_medium = urlparse.parse_qs(parameters_list.query).get('utm_medium', None)

        expires = max_age = 30 * 24 * 60 * 60 # one month
        if utm_source:
            ResponseMiddleWare.set_cookie(response, 'utm_source', utm_source[0], max_age, expires)

        if utm_medium:
            ResponseMiddleWare.set_cookie(response, 'utm_medium', utm_medium[0], max_age, expires)

        if utm_campaign:
            ResponseMiddleWare.set_cookie(response, 'utm_campaign', utm_campaign[0], max_age, expires)

        return response

    @staticmethod
    def set_cookie(response, key, value, max_age, expires):
        response.set_cookie(key, value, max_age=max_age, expires=expires,
                            domain=settings.SESSION_COOKIE_DOMAIN,
                            secure=settings.SESSION_COOKIE_SECURE or None)
