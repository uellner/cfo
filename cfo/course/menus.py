from menu import Menu, MenuItem
from .models import Course, Unit, Lesson, Activity
from django.core.urlresolvers import reverse

course = Course.objects.get(id=1)
units = Unit.objects.filter(course=course)

for unit in units:
    lessons = Lesson.objects.filter(unit=unit)
    lesson_items = []
    for lesson in lessons:
        activities = Activity.objects.filter(lesson=lesson)
        activities_items = []
        for activity in activities:
            activities_items.append(
                MenuItem(
                    title=activity.title,
                    url=reverse("activity", args=[activity.id]),
                    weight=10,
                    icon="user"
                ),
            )
        lesson_items.append(
            MenuItem(
                title=lesson.title,
                url=reverse("index"),
                weight=10,
                icon="user",
                children=(
                    activities_items
                )
            ),
        )
    Menu.add_item(
        "unit",
        MenuItem(
            title=unit.title,
            url=reverse("index"),
            weight=10,
            icon="tools",
            children=(
                lesson_items
            )
        )
    )
