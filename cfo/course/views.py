from django.shortcuts import get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to
from .models import Activity, Unit, Lesson, Course
from ..user.models import CourseProgress, QuizProgress


@render_to('index.html')
@login_required
def index(request):
    return redirect('dashboard')


@render_to('dashboard.html')
@login_required
def dashboard(request):
    """ Dashboard """
    feature_course = get_object_or_404(Course, id=1)
    student = request.user.profile
    student_progress = CourseProgress.objects.filter(student=student).all()
    student_courses = [cp.course for cp in student_progress]
    next_activity = None
    quiz_progress = None
    if feature_course in student_courses:
        next_activity = feature_course.get_next_activity(student)
        feature_course_progress = CourseProgress.objects.filter(
            student=student, course=feature_course
        ).first()
        quiz_progress = QuizProgress.objects.filter(
            student=student,
            quiz__course=feature_course,
            is_completed=False
        ).all()
        if quiz_progress:
            quiz_progress = quiz_progress[0]
            print ("@" * 100)
            print (quiz_progress)
            print ("@" * 100)

    return {
        'course': feature_course,
        'student_courses': student_courses,
        'student_progress': student_progress,
        'feature_course_progress': feature_course_progress,
        'feature_quiz_progress': quiz_progress,
        'next_activity': next_activity,
        'user_logout': reverse('logout_view'),
    }


@login_required
def start_course(request, course_id):
    """ Start a course """
    course = get_object_or_404(Course, id=course_id)
    next_activity = course.start(request.user.profile)
    return redirect(
        reverse(
            'activity',
            args=(
                course.id,
                next_activity.lesson.id,
                next_activity.lesson.unit.id,
                next_activity.id
            )
        )
    )


@login_required
def resume_course(request, course_id):
    """ Resume a course """
    course = get_object_or_404(Course, id=course_id)
    current_activity = course.get_next_activity(request.user.profile)
    return redirect(
        reverse(
            'activity',
            args=(
                course.id,
                current_activity.lesson.id,
                current_activity.lesson.unit.id,
                current_activity.id
            )
        )
    )


@login_required
def finish_activity(request, course_id, activity_id):
    """ Finish an activity """
    activity = get_object_or_404(Activity, id=activity_id)
    student_progress = activity.finish(request.user.profile)
    if student_progress:
        current_unit = student_progress.activity.lesson.unit
        next_activity = student_progress.course.get_next_activity(
            request.user.profile
        )
        # Course is over
        if not next_activity:
            student_progress.course.finish(request.user.profile)
            return redirect('dashboard')
        # Unit is over
        if current_unit != next_activity.lesson.unit:
            return redirect(
                reverse('unit-finish', args=(course_id, current_unit.id))
            )
    else:
        # Error! What to do?
        pass
    return redirect(
        reverse(
            'activity',
            args=(
                next_activity.lesson.unit.course.id,
                next_activity.lesson.id,
                next_activity.lesson.unit.id,
                next_activity.id
            )
        )
    )


@render_to('activity.html')
@login_required
def activity(request, course_id, unit_id, lesson_id, id):
    activity = get_object_or_404(Activity, id=id)
    next_activity = (
        Activity.objects.filter(rank__gt=activity.rank)
        .filter(lesson=activity.lesson)
        .order_by('rank').first()
    )
    lesson_activities = Activity.objects.filter(
        lesson=activity.lesson
    ).exclude(id=activity.id).order_by('rank')
    return {
        'user_logout': reverse('logout_view'),
        'data': {
            'obj': activity,
            'lesson_activities': lesson_activities,
            'course': activity.lesson.unit.course,
            'unit': activity.lesson.unit,
            'lesson': activity.lesson,
            'next_id': next_activity and next_activity.id or activity.id,
        }
    }


@render_to('unit.html')
@login_required
def unit(request, course_id, id):
    unit = get_object_or_404(Unit, id=id)
    lessons = Lesson.objects.filter(unit=unit).order_by('rank')
    activities = Activity.objects.filter(lesson__unit=unit).order_by('lesson__rank', 'rank')
    course = get_object_or_404(Course, id=course_id)
    course_progress = CourseProgress.objects.filter(student=request.user.profile, course=course).all()
    if course_progress:
        course_progress = course_progress[0]
    return {
        'user_logout': reverse('logout_view'),
        'data': {
            'obj': unit,
            'summary': unit.summary,
            'rank': unit.rank,
            'lessons': lessons,
            'activities': activities,
            'course_progress': course_progress
        },
    }


@render_to('unit_finish.html')
@login_required
def unit_finish(request, course_id, id):
    unit = get_object_or_404(Unit, id=id)
    course = get_object_or_404(Course, id=course_id)
    next_activity = course.get_next_activity(request.user.profile)
    course_progress = CourseProgress.objects.filter(
        student=request.user.profile, course=course
    ).all()
    if course_progress:
        course_progress = course_progress[0]
    return {
        'user_logout': reverse('logout_view'),
        'data': {
            'obj': unit,
            'course': course,
            'next_activity': next_activity,
            'course_progress': course_progress
        },
    }


@render_to('course.html')
@login_required
def course(request, id):
    course = get_object_or_404(Course, id=id)
    units = Unit.objects.filter(course=course).order_by('rank')
    course_progress = CourseProgress.objects.filter(
        student=request.user.profile, course=course
    ).all()
    if not course_progress:
        next_activity = course.get_start_activity()
    else:
        course_progress = course_progress[0]
        next_activity = course.get_next_activity(request.user.profile)
    return {
        'user_logout': reverse('logout_view'),
        'data': {
            'obj': course,
            'next_activity': next_activity,
            'units': units,
            'course_progress': course_progress,
        },
    }
