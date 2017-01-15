from django.shortcuts import get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to
from .models import Quiz


@render_to('quiz.html')
@login_required
def start_quiz(request, course_id):
    # activity = get_object_or_404(Activity, id=id)
    return {
        'user_logout': reverse('logout_view'),
        'data': {
            'course': 'teste',
        }
    }
