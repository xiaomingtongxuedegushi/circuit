from django.contrib import admin
from data.models import Userinfo, Classification, Fault,serial
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin

# Register your models here.

admin.site.site_header = '车辆智能一体化平台'
admin.site.site_title = '车辆智能一体化平台管理系统'

# admin.site.register(Userinfo)


@admin.register(Classification)
class ClassificationAdmin(admin.ModelAdmin):
    list_display = ['id','class_name']


@admin.register(Fault)
class FaultAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'name', 'card', 'address', 'status', 'belong_class']
    list_filter = ['card', 'belong_class']
    search_fields = ['name']
    list_editable = ['name', 'address']

@admin.register(serial)
class serialAdmin(admin.ModelAdmin):
    list_display= ['name','port']