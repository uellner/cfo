from django.shortcuts import get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to
from .models import Quiz, QuizProgress, QuizQuestion, Answer
from .forms import AnswerQuizForm
from ..course.models import Unit


@render_to('quiz.html')
@login_required
def start_unit_quiz(request, unit_id):
    unit = get_object_or_404(Unit, id=unit_id)

    # Checking if already exists a quiz in progress for the student and unit
    quiz_progress = QuizProgress.objects.filter(
        student=request.user.profile,
        is_completed=False,
        quiz__unit=unit.id
    ).all()

    # I's not possible to create a quiz while there is another one in progress
    if quiz_progress and quiz_progress[0]:
        return redirect(reverse('dashboard'))

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

    return redirect(reverse('resume-quiz', args=(quiz_progress.id,)))


@render_to('quiz.html')
@login_required
def resume(request, quiz_progress_id):
    quiz_progress = get_object_or_404(QuizProgress, id=quiz_progress_id)
    # if the user is not the student
    if not quiz_progress.student == request.user.profile:
        return redirect(reverse('dashboard'))
    # if the quiz is finished...
    if quiz_progress.is_completed:
        return redirect(reverse('dashboard'))

    # find the current answer
    current_question = QuizQuestion.objects.filter(
        quiz=quiz_progress.quiz,
        number=quiz_progress.progress + 1
    ).all()
    current_question = current_question and current_question[0] or None

    # the quiz needs to be finished ...
    # TODO finish a quiz!
    if not current_question:
        return redirect(reverse('dashboard'))

    answers = Answer.objects.filter(question=current_question.question).all()

    if request.method == 'POST':
        form = AnswerQuizForm(answers, request.POST)
        if form.data['answers']:
            # get the answer
            answer_id = int(form.data['answers'])
            answer = get_object_or_404(Answer, id=answer_id)
            # save the answer and progress
            quiz_progress.save_progress(answer)

            return redirect(reverse('resume-quiz', args=(quiz_progress_id)))
    else:
        form = AnswerQuizForm(answers)

    return {
        'user_logout': reverse('logout_view'),
        'action': reverse('resume-quiz', args=(quiz_progress_id)),
        'form': form,
        'data': {
            'unit': quiz_progress.quiz.unit,
            'quiz_progress': quiz_progress,
            'current_question': current_question,
            'answers': answers
        }
    }
