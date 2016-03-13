from django.shortcuts import get_object_or_404
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
    return {
        'user_logout': reverse('logout_view'),
        'activity_video': activity.video,
        'activity_title': activity.title
    }
