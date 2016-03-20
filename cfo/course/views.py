from django.shortcuts import get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to
from .models import Activity


@render_to('index.html')
@login_required
def index(request):
    return {
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
    prev_activity = (
        Activity.objects.filter(rank__lt=activity.rank)
        .filter(lesson=activity.lesson)
        .order_by('rank').first()
    )
    return {
        'user_logout': reverse('logout_view'),
        'activity_video': activity.video,
        'activity_title': activity.title,
        'next_id': next_activity and next_activity.id or activity.id,
        'prev_id': prev_activity and prev_activity.id or activity.id
    }


def next_or_prev(request):
    activity_id = None
    if 'next' in request.GET:
        activity_id = request.GET['next']
    if 'prev' in request.GET:
        activity_id = request.GET['prev']

    return redirect('activity', id=activity_id)
