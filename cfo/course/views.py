from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from .models import Lesson


@login_required
def index(request):
    lesson = Lesson.objects.get(id=1)
    return render(
        request,
        'index.html',
        {
            'user_logout': reverse('logout_view'),
            'lesson_video': lesson.video,
            'lesson_title': lesson.title
        }
    )
