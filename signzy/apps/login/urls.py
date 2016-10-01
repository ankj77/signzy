"""signzy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf import settings

# from api.login_api import LoginApi, SignupApi
from signzy.apps.login.api.login_api import SignupApi
from views.landing_views import LandingView


urlpatterns = [
    url(r'^$', LandingView.as_view(), name='home'),
    # url(r'^login/$', LoginApi.as_view(), name='login'),
    # url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^signup/$', SignupApi.as_view(), name='signup'),
]
