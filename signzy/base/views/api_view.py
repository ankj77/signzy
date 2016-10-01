from rest_framework.response import Response
from rest_framework.views import APIView

from signzy.common.constants import API


class SignzyApiView(APIView):
    def get_response(self, success, message='', payload={}, code=200, content_type='application/json'):
        if not success:
            data = {API.STATUS: API.ERROR, API.MESSAGE: message}
        else:
            data = {API.STATUS: API.SUCCESS, API.PAYLOAD: payload}
        return Response(data, status=code, content_type=content_type)
