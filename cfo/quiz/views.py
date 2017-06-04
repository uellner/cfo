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
    return {
        'user_logout': reverse('logout_view'),
        'data': {
            'unit': unit,
            'quiz_progress': quiz_progress
        }
    }


@render_to('quiz.html')
@login_required
def answer(request, quiz_progress_id, answer_id):
    # Tem que fazer um form pra responder isso ...
    quiz_progress = get_object_or_404(QuizProgress, id=quiz_progress_id)
    answer = get_object_or_404(Answer, id=answer_id)
    # save the answer and progress
    quiz_progress.answers.add(answer)
    quiz_progress.progress += 1
    if answer.is_correct:
        quiz_progress.score += 1
    quiz_progress.save()

    return redirect(
        reverse('resume', args=(quiz_progress_id))
    )


@render_to('quiz.html')
@login_required
def resume(request, quiz_progress_id):
    quiz_progress = get_object_or_404(QuizProgress, id=quiz_progress_id)
    current_question = QuizQuestion.objects.filter(
        quiz=quiz_progress.quiz,
        number=quiz_progress.progress + 1
    ).all()
    current_question = current_question and current_question[0]
    answers = Answer.objects.filter(question=current_question.question).all()

    return {
        'user_logout': reverse('logout_view'),
        'data': {
            'unit': quiz_progress.quiz.unit,
            'quiz_progress': quiz_progress,
            'current_question': current_question,
            'answers': answers
        }
    }
