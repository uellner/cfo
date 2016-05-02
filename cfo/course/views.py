from django.shortcuts import get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to
from .models import Activity, Unit, Lesson, Course


@render_to('index.html')
@login_required
def index(request):
    return redirect('dashboard')


@render_to('dashboard.html')
@login_required
def dashboard(request):
    course = get_object_or_404(Course, id=1)
    next_activity = Activity.objects.filter(lesson__unit__course=course).order_by('lesson__rank', 'rank')[0]
    return {
        'course': course,
        'next_activity': next_activity,
        'user_logout': reverse('logout_view'),
    }


@render_to('activity.html')
@login_required
def activity(request, id):
    activity = get_object_or_404(Activity, id=id)
    next_activity = (
        Activity.objects.filter(rank__gt=activity.rank)
        .filter(lesson=activity.lesson)
        .order_by('rank').first()
    )
    lesson_activities = Activity.objects.filter(lesson=activity.lesson).exclude(id=activity.id).order_by('rank')
    return {
        'user_logout': reverse('logout_view'),
        'activity_video': activity.video,
        'activity': activity,
        'lesson_activities': lesson_activities,
        'unit': activity.lesson.unit,
        'lesson': activity.lesson,
        'next_id': next_activity and next_activity.id or activity.id,
    }


def next_or_prev(request):
    activity_id = None
    if 'next' in request.GET:
        activity_id = request.GET['next']
    if 'prev' in request.GET:
        activity_id = request.GET['prev']

    return redirect('activity', id=activity_id)


@render_to('unit.html')
@login_required
def unit(request, id):
    unit = get_object_or_404(Unit, id=id)
    lessons = Lesson.objects.filter(unit=unit).order_by('rank')
    activities = Activity.objects.filter(lesson__unit=unit).order_by('lesson__rank', 'rank')
    return {
        'user_logout': reverse('logout_view'),
        'unit': {
            'title': unit.title,
            'summary': unit.summary,
            'rank': unit.rank,
            'lessons': lessons,
            'activities': activities
        },
    }


@render_to('course.html')
@login_required
def course(request, id):
    course = get_object_or_404(Course, id=id)
    units = Unit.objects.filter(course=course).order_by('rank')
    next_activity = Activity.objects.filter(lesson__unit__course=course).order_by('lesson__rank', 'rank')[0]
    return {
        'user_logout': reverse('logout_view'),
        'course': {
            'title': course.title,
            'summary': course.summary,
            'next_activity': next_activity,
            'units': units,
        },
    }
