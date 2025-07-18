from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from usermanage.models import Department, Classes, Students, Teachers
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from django.contrib.auth.models import User


# Register your models here.


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id','de_name']


@admin.register(Classes)
class ClassesAdmin(ImportExportModelAdmin):
    list_display = ['id', 'cl_name', 'belong_De']


@admin.register(Students)
class StudentsAdmin(ImportExportActionModelAdmin):
    list_display = ['sid', 'name', 'sex', 'belong_class']
    list_editable = ['name', 'sex', 'belong_class']
    search_fields = ['sid', 'name']
    list_filter = ['sex', 'belong_class']

class TeachersResource(resources.ModelResource):
    class Meta:
        model =Teachers
        exclude= ['belong_user']

@admin.register(Teachers)
class TeachersAdmin(ImportExportActionModelAdmin):
    list_display = ['enable','tid', 'name', 'sex', 'belong_De', 'belong_user']
    list_editable = ['enable', 'sex', 'belong_De', 'belong_user']
    search_fields = ['tid', 'name']
    list_display_links = ['name']
    list_filter = ['sex', 'belong_De']
    # resource_class=Teachers

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'belong_user':
            if not request.user.is_superuser:
                u = User.objects.filter(id__gt=1)
                kwargs['queryset'] = u
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class UserAdmin(BaseUserAdmin):
    list_display = ['id', 'username']

    # fields = ('username')
    # exclude = ['username']
    def get_queryset(self, request):
        us = super().get_queryset(request)
        if request.user.is_superuser:
            return us
        else:
            return us.filter(id__gt=1)

    def changelist_view(self, request, extra_context=None):
        # user = request.user
        if request.user.is_superuser:
            self.list_display = ['id', 'username']
        else:
            self.list_display = ['id', 'username']
            self.readonly_fields = [ 'Permissions', 'is_superuser', 'is_active', 'groups',
                                    'user_permissions']

        return super(UserAdmin, self).changelist_view(request, extra_context=None)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
