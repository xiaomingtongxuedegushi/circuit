from django.contrib import admin
from django.db.models import Q

from curriculum.models import Course, Resources, Resources_views
from django.utils.safestring import mark_safe


# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'enable', 'image_data', 'belong_tid']
    list_editable = ['enable']
    readonly_fields = ['image_data']
    search_fields = ['name']
    list_filter = ['belong_tid', 'enable']

    def get_queryset(self, request):

        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(~Q(type=1))
        else:
            return qs

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == 'type':
            if not request.user.is_superuser:
                kwargs['choices'] = ((0, '自建'),)
        return super().formfield_for_choice_field(db_field, request, **kwargs)


@admin.register(Resources)
class ResourcesAdmin(admin.ModelAdmin):
    list_display = ['belong_course', 'serial', 'name', 'file_type','views_html']
    list_filter = ['belong_course', 'file_type']
    search_fields = ['name']
    list_display_links = ['serial', 'belong_course']

    def get_queryset(self, request):

        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(~Q(type=1))
        else:
            return qs

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == 'type':
            if not request.user.is_superuser:
                kwargs['choices'] = ((0, '自建'),)
        return super().formfield_for_choice_field(db_field, request, **kwargs)

@admin.register(Resources_views)
class ResourcesAdminViews(admin.ModelAdmin):
    list_display = ['id', 'sid', 'belong_class', 'belong_resources', 'view_time']
    list_filter = ['belong_resources', 'sid', 'belong_class']
    search_fields = []

