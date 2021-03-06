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
from ..quiz import views as quiz_views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/',user_views.login_view, name='login_view'),
    url(r'^logout/',user_views.logout_view, name='logout_view'),
    url(r'^recover/',user_views.recover_view, name='recover_view'),
    url(r'^student/(?P<student>[0-9]+)/$', user_views.edit, name='user_edit'),
    url(r'^quiz/unit/(?P<unit_id>[0-9]+)/start/$', quiz_views.start_unit_quiz, name='start-unit-quiz'),
    url(r'^quiz/progress/(?P<quiz_progress_id>[0-9]+)/retake-unit-quiz/$', quiz_views.retake_unit_quiz, name='retake-unit-quiz'),
    url(r'^quiz/progress/(?P<quiz_progress_id>[0-9]+)/finish-unit-quiz/$', quiz_views.finish_unit_quiz, name='finish-unit-quiz'),
    url(r'^quiz/progress/(?P<quiz_progress_id>[0-9]+)/review/$', quiz_views.review, name='review-quiz'),
    url(r'^quiz/progress/(?P<quiz_progress_id>[0-9]+)/resume/$', quiz_views.resume, name='resume-quiz'),
    url(r'^quiz/progress/(?P<quiz_progress_id>[0-9]+)/score/$', quiz_views.score, name='score-quiz'),
    url(
        r'^course/(?P<course_id>[0-9]+)/unit/(?P<unit_id>[0-9]+)/lesson/(?P<lesson_id>[0-9]+)/activity/(?P<id>[0-9]+)/$',
        course_views.activity,
        name='activity'
    ),
    url(r'^course/(?P<course_id>[0-9]+)/unit/(?P<id>[0-9]+)/$', course_views.unit, name='unit'),
    url(r'^course/(?P<course_id>[0-9]+)/unit/(?P<id>[0-9]+)/finish/$', course_views.unit_finish, name='unit-finish'),
    url(r'^course/(?P<id>[0-9]+)/$', course_views.course, name='course'),
    url(r'^course/(?P<course_id>[0-9]+)/start/$', course_views.start_course, name='start_course'),
    url(r'^course/(?P<course_id>[0-9]+)/resume/$', course_views.resume_course, name='resume-course'),
    url(r'^course/(?P<course_id>[0-9]+)/finish-activity/(?P<activity_id>[0-9]+)/$', course_views.finish_activity, name='finish_activity'),
    url(r'^dashboard/', course_views.dashboard, name='dashboard'),
    url(r'^', course_views.index, name='index'),
]
