from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return render(
        request,
        'index.html',
        {
            'user_logout': reverse('logout_view')
        }
    )
