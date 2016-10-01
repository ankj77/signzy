import datetime
import logging

from base import log_args
from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView


logger = logging.getLogger(__name__)


class TreeboTemplateView(TemplateView):
    def get_template_names(self):
        return super(TreeboTemplateView, self).get_template_names()

    @log_args(logger)
    def get(self, request, *args, **kwargs):
        logger.debug('Session Key in TemplateView: %s', request.session.session_key)
        st = datetime.datetime.now()
        isMobile = False
        if hasattr(request, 'is_mobile') and request.is_mobile:
            if hasattr(self,
                       'redirect_mobile_to_desktop_view') and self.redirect_mobile_to_desktop_view:
                isMobile = False
            else:
                isMobile = True
        request.session['is_mobile'] = isMobile
        if isMobile:
            context = self.getMobileData(request, args, kwargs)
            self.template_name = 'mobile/' + self.template_name
        else:
            context = self.getData(request, args, kwargs)
            self.template_name = 'desktop/' + self.template_name

        et = datetime.datetime.now()


        if isinstance(context, HttpResponseRedirect):
            return context

        context["GTM_KEY"] = settings.GTM_KEY
        context['environment'] = settings.ENVIRONMENT
        context['MAPS_KEY'] = settings.MAPS_KEY
        if isinstance(context, dict):
            if (context.get('jsvars') != None):
                request.jsvars = context.get('jsvars')

        logger.info("Controller %s took %s seconds" % (str(self.__class__.__name__), (et - st).microseconds/1000))

        logger.info("Controller {api} took {time} seconds", extra={"api": str(self.__class__.__name__), "time": (et - st).microseconds/1000})

        return self.render_to_response(context)

    @log_args(logger)
    def getData(self, request, args, kwargs):
        return None

    @log_args(logger)
    def getMobileData(self, request, args, kwargs):
        """
            Return the data need by the mobile template
        :rtype : dict
        :param request:
        :param args:
        :param kwargs:
        :return: dict of values.
        """
        return None

    @log_args(logger)
    def post(self, request, *args, **kwargs):
        data = request.POST
        st = int(datetime.datetime.now().strftime('%s'))
        isMobile = False
        if hasattr(request, 'is_mobile') and request.is_mobile:
            if hasattr(self, 'redirect_mobile_to_desktop_view') and self.redirect_mobile_to_desktop_view:
                isMobile = False
            else:
                isMobile = True
        request.session['is_mobile'] = isMobile
        if isMobile:
            context = self.postMobileData(request, args, kwargs)
            if self.template_name:
                self.template_name = 'mobile/' + self.template_name
        else:
            context = self.postData(request, args, kwargs)
            if self.template_name:
                self.template_name = 'desktop/' + self.template_name

        et = int(datetime.datetime.now().strftime('%s'))
        logger.info("Controller %s took %s seconds" % (str(self.__class__.__name__), et - st))

        if isinstance(context, HttpResponseRedirect):
            return context
        return self.render_to_response(context)

    @log_args(logger)
    def postData(self, request, args, kwargs):
        return None

    @log_args(logger)
    def postMobileData(self, request, args, kwargs):
        """
            Return the data need by the mobile template
        :rtype : dict
        :param request:
        :param args:
        :param kwargs:
        :return: dict of values.
        """
        return None
