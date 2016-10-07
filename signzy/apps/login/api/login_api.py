import datetime

from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import BasicAuthentication

from signzy.apps.login.model_helpers.disable import SessionCsrfExemptAuthentication
from signzy.base.views.api_view import SignzyApiView
from signzy.apps.login.services.login_service import LoginService
from ..models.form import LoginForm, SignupForm


class LoginApi(SignzyApiView):
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        raise Exception

    def post(self, request, *args, **kwargs):
        MyLoginForm = LoginForm(request.data)
        if MyLoginForm.is_valid():
            username_or_email = MyLoginForm.cleaned_data['username']
            password = MyLoginForm.cleaned_data['password']
            try:
                payload = LoginService.validate_login(request, username_or_email, password)
                response = self.get_response(True, payload=payload)
            except Exception as e:
                response = self.get_response(False, message=str(e))
        else:
            response = self.get_response(False, message=MyLoginForm.errors)
        return response


class SignupApi(SignzyApiView):
    def get(self, request, *args, **kwargs):
        raise Exception

    def post(self, request, *args, **kwargs):
        signupForm = SignupForm(request.data)
        json_data = request.data
        print json_data
        print type(json_data)
        if signupForm.is_valid():
            username = signupForm.cleaned_data['username']
            email = signupForm.cleaned_data['email']
            password = signupForm.cleaned_data['password']
            first_name = signupForm.cleaned_data['first_name']
            last_name = signupForm.cleaned_data['last_name']
            phone = signupForm.cleaned_data['phone']
            gender = signupForm.cleaned_data['gender']
            member_type = signupForm.cleaned_data['member_type']
            is_staff = signupForm.cleaned_data['is_staff']
            is_verified = signupForm.cleaned_data['is_verified']
            print "user " + str(username)
            print "email " + str(email)
            print "password " + str(password)
            print "first_name " + str(first_name)
            print "last_name " + str(last_name)
            print "phone " + str(phone)
            print "gender " + str(gender)
            print "member_type " + str(member_type)
            print "is_staff " + str(is_staff)
            print "is_verified " + str(is_verified)
            login_service = LoginService()
            try:
                payload = login_service.validate_signin(request, username, email, password, first_name, last_name,
                                                        phone,
                                                        gender,
                                                        member_type,
                                                        is_staff, is_verified)
                return self.get_response(True, payload=payload)
            except Exception as e:
                print e
                response = self.get_response(False, message=str(e))
        else:
            print "fail"
            response = self.get_response(False, message=signupForm.errors)
        return response
