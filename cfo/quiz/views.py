from django.shortcuts import get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to
from .models import Quiz, QuizProgress, QuizQuestion, Answer
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

    # start the quiz
    quiz_progress = new_quiz.start(
        student=request.user.profile,
        sample=2,
        units=[unit_id]
    )
    if quiz_progress:
        print("@" * 100)
        print(quiz_progress)
        print("@" * 100)

    return {
        'user_logout': reverse('logout_view'),
        'data': {
            'unit': unit,
            'quiz_progress': quiz_progress
        }
    }


@render_to('quiz.html')
@login_required
def resume_quiz(request, quiz_progress_id):
    quiz_progress = get_object_or_404(QuizProgress, id=quiz_progress_id)
    answers = None
    if quiz_progress:
        current_question = QuizQuestion.objects.filter(
            quiz=quiz_progress.quiz,
            number=quiz_progress.answer + 1
        ).all()
        current_question = current_question and current_question[0]
        answers = Answer.objects.filter(question=current_question.question).all()
    return {
        'user_logout': reverse('logout_view'),
        'data': {
            'quiz_progress': quiz_progress,
            'current_question': current_question,
            'answers': answers
        }
    }
