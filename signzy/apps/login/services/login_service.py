from django.db.models.query_utils import Q
from datetime import datetime
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import BasicAuthentication

from signzy.apps.login.model_helpers.disable import SessionCsrfExemptAuthentication
from signzy.apps.login.models.user_profile import User
from signzy.common.constants import UtilsConstant, API
from signzy.common.exceptions import ExceptionMessage


@csrf_exempt
class LoginService:



    # @staticmethod
    def validate_login(self,request, username_or_email, password):
        print "username_or_email " + str(username_or_email)
        print "password " + str(password)
        is_email = UtilsConstant.EMAIL_REGEX.match(username_or_email)
        if not is_email:
            print "user %s ", username_or_email
            print "password %s ", password
            user = User.authenticate(username=username_or_email, password=password)
        else:
            username_or_email = self.__strip_gmail_special_chars(username_or_email)
            user = authenticate(email=username_or_email, password=password)
        if user:
            if user.is_active:
                login(request, user)
                request.session['user'] = user.email
                payload = {API.SUCCESS: True, 'first_name': user.first_name, 'last_name': user.last_name,
                           'email': user.email,
                           'username': user.username, 'phone': user.phone, 'gender': user.gender,
                           'member_type': user.member_type, 'is_active': user.is_active,
                           'is_verified': user.is_verified, 'is_staff': user.is_staff}
            else:
                payload = {API.SUCCESS: False,
                           API.MESSAGE: ExceptionMessage.INACTIVE_USER}
        else:
            payload = {
                API.SUCCESS: False,
                API.MESSAGE: ExceptionMessage.USER_PASSWORD_MISMATCH}
        return payload

    # @staticmethod
    def validate_signin(self,request, username, email, password, first_name, last_name, phone, gender, member_type,
                        is_staff,
                        is_verified):

        user = self.get_existing_user(username, email)
        if user:
            print "user is present"
            payload = {
                API.SUCCESS: False, API.MESSAGE: ExceptionMessage.USER_ALREADY_PRESENT
            }
        else:
            print "user new "
            # login(request, user)
            # request.session.flush()
            # request.session['user'] = email
            # login(request,user)
            print "user session "
            # user = User.objects.create_user(email=email)
            user = User(email=email, username=username)
            # user.username = username
            print "user UserProfile "
            user.first_name = first_name
            user.last_name = last_name
            user.phone = phone
            if (gender.lower() == 'female'):
                user.gender = User.FEMALE
            else:
                user.gender = User.MALE

            if ('alumni' in member_type.lower()):
                user.member_type = User.ALUMNI
            else:
                user.member_type = User.STUDENT
            user.is_active = True
            user.is_staff = is_staff
            user.is_verified = is_verified

            print "user is_verified "
            user.set_password(password)
            user.last_login = datetime.now()
            print "user set_password "
            user.save()
            print "user save "
            payload = {API.SUCCESS: True, 'first_name': user.first_name, 'last_name': user.last_name,
                       'email': user.email,
                       'username': user.username, 'phone': user.phone, 'gender': user.gender,
                       'member_type': user.member_type, 'is_active': user.is_active,
                       'is_verified': user.is_verified, 'is_staff': user.is_staff}
        return payload

    def get_existing_user(self,username, email):
        # email = LoginService.__strip_gmail_special_chars(email)
        user = User.objects.filter(Q(username=username) | Q(email=email)).first()
        # user = User.objects.filter(email=email).first()
        return user

    # @staticmethod
    def __strip_gmail_special_chars(self,email):
        import re
        if "gmail" in email:
            stripped_email = email.replace("@gmail.com", "")
            stripped_email = re.sub(r"\+.*", "", stripped_email, flags=re.IGNORECASE)
            return stripped_email.replace(".", "") + "@gmail.com"
        return email


"""
{
  "success": true,
  "payload": {
    /* Application-specific data would go here. */
  }
}
Failed request:

{
  "success": false,
  "payload": {
    /* Application-specific data would go here. */
  },
          "error": {
            "code": 123,
            "message": "An error occurred!"
          }
        }


        """
