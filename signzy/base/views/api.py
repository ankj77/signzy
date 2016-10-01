import datetime
import logging

from django.conf import settings
from rest_framework.exceptions import ValidationError
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.views import APIView

from base.renderers import TreeboJSONRenderer
from common.exceptions.treebo_exception import TreeboValidationException

logger = logging.getLogger(__name__)


class TreeboAPIView(APIView):
    renderer_classes = (TreeboJSONRenderer,)

    validationSerializer = None
    serializerObject = None

    def initialize_request(self, request, *args, **kwargs):
        request = super(TreeboAPIView, self).initialize_request(request, *args, **kwargs)
        if settings.DEBUG:
            self.renderer_classes += (BrowsableAPIRenderer,)
        if request.method == 'GET':
            data = request.GET
        else:
            data = request.data

        method = request.method.lower()
        if self.validationSerializer:
            if isinstance(self.validationSerializer,
                          dict) and method in self.validationSerializer and \
                self.validationSerializer[method]:
                self.serializerObject = self.validationSerializer[method](data=data)
            else:
                self.serializerObject = self.validationSerializer(data=data)

            try:
                self.serializerObject.is_valid(raise_exception=True)
            except ValidationError as e:
                raise TreeboValidationException(e.detail.itervalues().next()[0])
        return request

    def dispatch(self, request, *args, **kwargs):
        # TODO: ideally data should be request.data, dunno why its not working, fix it - Kaddy

        # FIXED: request.data is present in DRF Request object, which is created by initialize_request method of APIView.
        # dispatch method receives an HttpRequest object. The initialize_request method is called from dispatch method.
        # So, we can move the request validation to initialize_request method above.
        st = datetime.datetime.now()
        dispatcherResponse = super(TreeboAPIView, self).dispatch(request, *args, **kwargs)
        et = datetime.datetime.now()
        logger.info("API %s took %s seconds" % (str(self.__class__.__name__), (et - st).microseconds/1000))

        logger.info("API {api} took {time} seconds", extra={"api": str(self.__class__.__name__), "time": (et - st).microseconds/1000})

        logger.info("API end " + str(self.__class__.__name__))

        return dispatcherResponse
