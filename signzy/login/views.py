from django.shortcuts import render
from rest_framework.views import APIView


class LandingView(APIView):

    def get(self, request, *args, **kwargs):
        print "Landing Page"
        session = request.session.has_key('username')
        if session:
            username = request.session['username']
            return render(request,'tindex.html' , {"username": username})
        else:
            return render(request, 'tindex.html', {})

