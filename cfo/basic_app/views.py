from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import View, DeleteView
from django_tables2 import RequestConfig
from django.contrib import messages
from django.core.urlresolvers import resolve
from django.core.urlresolvers import reverse
from django.conf import settings
from annoying.decorators import render_to
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin
from wkhtmltopdf.views import PDFTemplateView
from django.template.context import RequestContext


class BasicPdf(PDFTemplateView):
    """ Basic view class to render pdfs.
    """
    show_content_in_browser = settings.DEBUG
    data = {}
    cmd_options = {}

    def get(self, request, *args, **kwargs):
        if hasattr(self, 'update_data'):
            self.request = request
            self.update_data(request, *args, **kwargs)
            self.data['is_pdf'] = self.data.get('is_pdf', True)
        return super(BasicPdf, self).get(request, *args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        """
        Returns a PDF response with a template rendered with the given context.
        """
        context = RequestContext(
            self.request, {'data': self.data,}
        )
        return super(BasicPdf, self).render_to_response(context, **response_kwargs)


class BasicList(PermissionRequiredMixin, View):
    """
        View Class básica para renderizar uma lista com opção de filtros.

        model django.models: Model utilizado para mostrar os dados.
        table django_tables2.table: Definição da Tabela utilizada pelo plugin django_tables2.
        queryset query: query utilizada para obter os dados.
        filterset django_filters: filtro para busca nos dados da tabela. Obtido
        a partir do plugin django-filters.
    """
    raise_exception = True
    permission_required = ''
    template_name = "list.html"
    per_page = 15
    model = None
    queryset = None
    filterset = None
    table = None
    add_new = None
    extra_filters = None

    def get(self, request, **kw):
        filters = None
        if self.extra_filters and callable(self.extra_filters):
            self.queryset = self.extra_filters(request, self.queryset)
        if self.filterset:
            filters = self.filterset(request.GET, queryset=self.queryset)
            table = self.table(filters)
        else:
            table = self.table(self.queryset)
        RequestConfig(request, paginate={'per_page': self.per_page}).configure(table)
        return render(
            request,
            self.template_name,
            {
                "table": table,
                'filters': filters,
                "breadcrumb_data": {
                    "current_label": self.model._meta.verbose_name_plural.title(),
                    "current_viewname": resolve(request.path_info).url_name
                },
                'add_new': self.add_new,
            }
        )


class BasicEdit(PermissionRequiredMixin, View):
    """
        View Class básica para edição de um formulário. Contém dos métodos GET e POST.

        model django.models: Model utilizado para mostrar os dados.
        form django.forms: Form utilizado.
        redirect_to str: url para redirecionamento da página.
        delete_url str: nome da url para o botão de remover.
        breadcrumbs dict: breadcrumbs para a página anterior.
    """
    raise_exception = True
    permission_required = ''
    template_name = "edit.html"
    model = None
    form = None
    redirect_to = None
    delete_url = None
    tabs = []
    breadcrumbs = {}

    def get(self, request, id=None, **kw):
        obj = None
        if id:
            obj = get_object_or_404(self.model, id=id)
            form = self.form(instance=obj)
            delete_url = self.delete_url and reverse(self.delete_url, args=[id])
        else:
            form = self.form()
        return render(
            request,
            self.template_name,
            {
                'form': form,
                'remove_url': id and delete_url or None,
                'tabs': id and self._add_tabs(request, obj) or [],
                "breadcrumb_data": {
                    'previous_label': self.breadcrumbs["previous_label"],
                    'previous_viewname': self.breadcrumbs["previous_view"],
                    'current_label': obj or "Adicionar",
                    'current_viewname': resolve(request.path_info).url_name,
                },
            }
        )

    @method_decorator(render_to(template_name))
    def post(self, request, id=None, **kw):
        obj = None
        if id:
            obj = get_object_or_404(self.model, id=id)
            form = self.form(request.POST, instance=obj)
            if not self.redirect_to:
                _redirect_to = resolve(request.path_info).url_name
        else:
            form = self.form(request.POST)
            _redirect_to = self.redirect_to

        if form.is_valid():
            obj = form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                form.messages.get("save")
            )
            return redirect(_redirect_to, id=obj.id)
        else:
            return {
                'form': form,
                'breadcrumb_data': {
                    'previous_label': self.breadcrumbs["previous_label"],
                    'previous_viewname': self.breadcrumbs["previous_view"],
                    'current_label': obj or "Adicionar",
                    'current_viewname': resolve(request.path_info).url_name,
                },
            }

    def _add_tabs(self, request, obj):
        """
            Metodo que adiciona abas no form quando necessário.

            obj: objeto principal do form.
            self.tabs = [dict(
                model django.models: Model utilizado para listar os dados.
                table django_tables2.table: Tabela utilizada pelo plugin django_tables2.
                relation_field str: Nome da relação entre os modelos.
                action_view str (option): Nome da view para o modal de adicionar novo.
            )]
        """
        _tabs = []
        for tab in self.tabs:
            if all(k in tab for k in ("model", "table", "relation_field")):
                _relation_field = tab["relation_field"] + '__exact'
                _search_value = obj.id
                obj_table = tab["table"](
                    tab["model"].objects.filter(**{_relation_field:_search_value})
                )
                RequestConfig(request).configure(obj_table)
                actions = []
                if "action_view" in tab:
                    actions = [
                        {
                            'selector': 'a',
                            'label': 'Adicionar',
                            'css_classes': ['btn', 'btn-primary', 'btn-sm'],
                            'attrs': "data-href='/%s/new/?id=%s' data-toggle='modal'"
                            % (tab["action_view"], obj.id)
                        }
                    ]
                _tabs.append(
                    dict(
                        label=tab["model"]._meta.verbose_name_plural.title(),
                        table=obj_table,
                        actions=actions,
                    )
                )
        return _tabs


class BasicDelete(PermissionRequiredMixin, DeleteView):
    """
        View Class básica para deletar um registro do banco de dados.

        model django.models: Model utilizado para obter os dados.
        form django.forms: Form utilizado.
        success_url str: url para redirecionamento da página após a remoção.
    """
    raise_exception = True
    permission_required = ''
    model = None
    form = None
    success_url = None
    template_name_suffix = None

    def get(self, request, id, **kw):
        obj = get_object_or_404(self.model, id=id)
        obj.delete()
        messages.add_message(
            request,
            messages.INFO,
            self.form().messages.get("remove")
        )
        return redirect(self.success_url)
