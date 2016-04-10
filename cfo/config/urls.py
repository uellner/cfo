"""cfo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from ..course import views as course_views
from ..user import views as user_views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/',user_views.login_view, name='login_view'),
    url(r'^logout/',user_views.logout_view, name='logout_view'),
    url(r'^recover/',user_views.recover_view, name='recover_view'),
    url(r'^activity/(?P<id>[0-9]+)/$', course_views.activity, name='activity'),
    url(r'^next_or_prev/',course_views.next_or_prev, name='next_or_prev'),
    url(r'^unit/(?P<id>[0-9]+)/$', course_views.unit, name='unit'),
    url(r'^course/(?P<id>[0-9]+)/$', course_views.course, name='course'),
    url(r'^', course_views.index, name='index'),
]
