
from django.contrib import admin
from django.contrib.admin.options import csrf_protect_m
from django.db import transaction


class RemovedModelAdmin(admin.ModelAdmin):
    actions = None
    exclude = ('is_removed',)

    @csrf_protect_m
    @transaction.atomic
    def delete_view(self, request, object_id, extra_context=None):
        # if request.POST is set, the user already confirmed deletion
        extra_context = {
            'deleted_objects': [],
            'model_count': [],
            'perms_needed': [],
            'protected': [],
        }
        return super(RemovedModelAdmin, self).delete_view(request, object_id, extra_context)


class EditOnlyModelAdmin(admin.ModelAdmin):
    actions = None

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
