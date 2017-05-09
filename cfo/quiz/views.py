from django.shortcuts import get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to
from .models import Quiz, Question, QuizQuestion
from ..course.models import Unit


@render_to('quiz.html')
@login_required
def start_unit_quiz(request, unit_id):
    unit = get_object_or_404(Unit, id=unit_id)
    # create a new quiz
    new_quiz = Quiz(
        course=unit.course,
        unit=unit,
    )
    new_quiz.save()
    # save the questions on new quiz
    for obj in Question.objects.random(2, [unit.id]).all():
        quiz_question = QuizQuestion(
            quiz=new_quiz,
            question=obj
        )
        quiz_question.save()
    return {
        'user_logout': reverse('logout_view'),
        'data': {
            'unit': unit,
        }
    }
