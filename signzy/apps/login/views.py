from django.shortcuts import render
from rest_framework.views import APIView


class LandingView(APIView):
    def get(self, request, *args, **kwargs):
        print "Landing Page"
        session = request.session.has_key('email')
        if session:
            email = request.session['email']
            return render(request, 'tindex.html', {"email": email})
        else:
            return render(request, 'tindex.html', {})
