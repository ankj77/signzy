import datetime

from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User

from login.constants import UserConstant
from login.models.form import LoginForm, SignupForm
from utils.constants import UtilsConstant, ApiConstant


class LoginApi(APIView):
    def get(self, request, *args, **kwargs):
        raise Exception

    def post(self, request, *args, **kwargs):
        MyLoginForm = LoginForm(request.data)
        if MyLoginForm.is_valid():
            username_or_email = MyLoginForm.cleaned_data['username']
            password = MyLoginForm.cleaned_data['password']

            if UtilsConstant.EMAIL_REGEX.match(username_or_email):
                try:
                    user = User.objects.get(email=username_or_email)
                except:
                    data = {ApiConstant.STATUS: ApiConstant.SUCCESS, ApiConstant.MESSAGE: UserConstant.USER_NOT_FOUND}
                    return Response(data)

            else:
                try:
                    user = User.objects.get(username=username_or_email)
                except:
                    data = {ApiConstant.STATUS: ApiConstant.SUCCESS, ApiConstant.MESSAGE: UserConstant.USER_NOT_FOUND}
                    return Response(data)

            is_success = False
            user = authenticate(username=user.username, password=password)
            if user:
                is_success = True

            if is_success:
                data = {ApiConstant.STATUS: ApiConstant.SUCCESS, ApiConstant.MESSAGE:
                    {'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email,
                     'username': user.username}}
                request.session['email'] = user.email
            else:
                data = {ApiConstant.STATUS: ApiConstant.SUCCESS,
                        ApiConstant.MESSAGE: UserConstant.USER_PASSWORD_MISMATCH}
            print "user " + str(username_or_email) + " pss " + str(password)

        else:
            data = {ApiConstant.STATUS: ApiConstant.ERROR, ApiConstant.MESSAGE: LoginForm.errors}
        return Response(data)


class SignupApi(APIView):
    def get(self, request, *args, **kwargs):
        raise Exception

    def post(self, request, *args, **kwargs):
        signupForm = SignupForm(request.data)
        if signupForm.is_valid():
            username = signupForm.cleaned_data['username']
            email = signupForm.cleaned_data['email']

            try:
                user_with_email = User.objects.get(email=email)
                return Response(
                    {ApiConstant.STATUS: ApiConstant.SUCCESS, ApiConstant.MESSAGE: UserConstant.USER_ALREADY_PRESENT})
            except:
                pass

            try:
                user_with_username = User.objects.get(username=username)
                return Response(
                    {ApiConstant.STATUS: ApiConstant.SUCCESS, ApiConstant.MESSAGE: UserConstant.USER_ALREADY_PRESENT})
            except:
                pass

            password = signupForm.cleaned_data['password']
            user = User.objects.create_user(username, email, password)
            user.first_name = signupForm.cleaned_data['first_name']
            user.last_name = signupForm.cleaned_data['last_name']
            user.last_login = datetime.datetime.now()
            user.save()
            request.session['email'] = email
            return Response({ApiConstant.STATUS: ApiConstant.SUCCESS, ApiConstant.MESSAGE: UserConstant.SIGNUP_SUCCESS})
        else:
            return Response({ApiConstant.STATUS: ApiConstant.ERROR, ApiConstant.MESSAGE: signupForm.errors})


class LogoutView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            del request.session['email']
            data = {ApiConstant.STATUS: ApiConstant.SUCCESS}
        except:
            data = {ApiConstant.STATUS: ApiConstant.ERROR}
        return Response(data)
