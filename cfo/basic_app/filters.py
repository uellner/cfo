from django.db.models import Q
from functools import reduce
import operator
import django_filters
from django.forms import widgets


class DefaultFilter(django_filters.FilterSet):
    """
        Classe base que representa os filtros que serão aplicados nos modelos.
    """
    all_fields = django_filters.MethodFilter(
        action='_search_fields_filter',
        label='',
        help_text='',
        widget=widgets.TextInput(
            attrs={
                'placeholder': 'Pesquisa...',
                'class': 'form-control search_field'}

        )
    )

    class Meta:
        model = None
        fields = {}

    search_fields = {}

    def _search_fields_filter(self, queryset, value):
        """
            Método que realiza o filtro em diversos campos declarados no
            atributo search_fields.
        """
        query_list = [
            Q((_search_field + _lookup_type, value)) for _search_field, _lookup_type in self.search_fields.items()
        ]
        return queryset.filter(
            reduce(operator.or_, query_list)
        )
