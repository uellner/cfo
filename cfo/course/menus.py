from menu import Menu, MenuItem
from django.core.urlresolvers import reverse

Menu.add_item(
    "course",
    MenuItem(
        title="Cursos",
        url=reverse("index"),
        weight=10,
        icon="tools",
        children=(
            MenuItem(
                "Adicionar Novo",
                reverse("index"),
                weight=10,
                icon="user"
            ),
            MenuItem(
                "Todos",
                reverse("index"),
                weight=10,
                icon="user"
            ),
        )
    )
)
