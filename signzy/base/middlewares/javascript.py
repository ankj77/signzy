import datetime
import json
import logging
import os.path

from django.conf import settings
from django.core.urlresolvers import resolve
from ipware.ip import get_ip

from apps.pricing.feature_toggle_api import FeatureToggleAPI
from webapp.analytics_tracker import config as constants

logger = logging.getLogger(__name__)

env = getattr(settings, "STATIC_URL", None)


class BaseJsObjMiddleware(object):
    # Adds the global 'rt' object to request
    def process_request(self, request):
        request.isReferralEnabled = FeatureToggleAPI.is_enabled("referral", "isReferralEnabled",
                                                                False)
        request.baseJsObj = json.dumps(self.getBaseJSObj(request))


    def load_analytics_events_config(self, request):
        event_config = {}
        isMobile = self.get_channel(request)
        if "rest/" not in request.path:
            pageConfig = self.getPageConfig(resolve(request.path), isMobile)
            try:
                if pageConfig is None:
                    return event_config

                page_id = pageConfig.get('page_id', None)
                if pageConfig is not None and page_id is not None:
                    analyticsConfigObj = constants.CLIENT_SIDE_EVENTS_LOAD.get(page_id, {})
                    for includeConfig in pageConfig.get('include_list'):
                        mergeInformation = constants.CLIENT_SIDE_EVENTS_LOAD.get(includeConfig, {})
                        self.mergeAnalyticsConfig(analyticsConfigObj, mergeInformation)
                    event_config = analyticsConfigObj
                else:
                    event_config = {}
            except Exception, e:
                logger.error(str(e))
        return event_config

    def get_channel(self, request):
        if hasattr(request, 'is_mobile') and request.is_mobile is True:
            isMobile = '1'
        else:
            isMobile = '0'
        return isMobile

    ## Function to merge page events.
    def mergeAnalyticsConfig(self, origConfigDict, mergeConfig):
        try:
            self.addUniqueElemetsDict(origConfigDict.get("available_elements"),
                                      mergeConfig.get("available_elements"))
            self.addUniqueElemetsDict(origConfigDict.get("element_override"),
                                      mergeConfig.get("element_override"))
            self.addUniqueElementsList(origConfigDict.get('events_list'),
                                       mergeConfig.get("events_list"))
        except Exception, err:
            logger.exception("Exception in mergeAnalyticsConfig")

    def addUniqueElemetsDict(self, origDict, mergeDict):
        for element in mergeDict:
            if origDict.get(element, None) is None:
                origDict[element] = mergeDict[element]

    def addUniqueElementsList(self, origList, mergeList):
        for element in mergeList:
            if element not in origList:
                origList.append(element)

    def getBaseJSObj(self, request):
        baseObj = {
        }
        baseObj['staticPath'] = env
        baseObj['analytics'] = {
            'identifier': str(
                request.user.id)} if request.user and request.user.is_authenticated() else {
            'identifier': str(request.session.session_key)}
        baseObj['analytics']['segment_io_key'] = settings.SEGMENT_EVENTS_KEY
        requestPath = request.path
        isMobile = self.get_channel(request)
        baseObj['analytics']['ISMOBILE'] = True if isMobile == "1" else False
        baseObj['analytics']['utm_params'] = request.session.get(
            'utm_params') if request.session.get(
            'utm_params') else {}
        baseObj['fbAppId'] = settings.FACEBOOK_APP_ID
        baseObj['loggedin'] = True if request.user and request.user.is_authenticated() else False
        baseObj[
            'userId'] = request.user.id if request.user and request.user.is_authenticated() else ""
        baseObj['user'] = self.get_user(
            request.user) if request.user and request.user.is_authenticated() else {}
        ip = get_ip(request)
        if ip is not None:
            baseObj['analytics']['IP'] = ip
        baseObj['analytics']['TIMESTAMP'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M %p')
        baseObj['analytics']['channel'] = 'mobile' if isMobile == '1' else 'desktop'
        baseObj['analytics']['event_date'] = datetime.datetime.today().strftime('%Y-%m-%d')
        baseObj['analytics']['event_time'] = datetime.datetime.now().strftime('%H:%M %p')
        baseObj['analytics']['config'] = self.load_analytics_events_config(request)
        return baseObj

    def get_user(self, user):
        return {'email': user.email, 'phone': user.phone_number, 'firstName': user.first_name}

    def getPageConfig(self, resolver_match, isMobile):
        try:
            requestSrc = constants.DEVICE_TO_CONFIG_MAP.get(isMobile, "DEFAULT")
            actionInfo = constants.ACTION_TO_EVENTS_MAPPER[requestSrc].get(
                "{0}:{1}".format(resolver_match.namespace, resolver_match.url_name), None)
            if actionInfo:
                return actionInfo
            else:
                actionInfo = constants.ACTION_TO_EVENTS_MAPPER[requestSrc].get(resolver_match, None)
                return actionInfo
        except Exception, e:
            logger.exception("Exception in getPageConfig")
            return None

    def generate_sections_of_url(self, resolver_match):
        sections = []
        temp = ""
        while resolver_match != '/':
            temp = os.path.split(resolver_match)
            resolver_match = temp[0]
            sections.append(temp[1])
        return sections
