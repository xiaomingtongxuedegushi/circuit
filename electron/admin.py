from django.contrib import admin
from electron.models import elecontest, EleRecord, Choice_ele, Multiple_ele, Judge_ele, Choice_res_ele, \
    Multiple_res_ele, Judge_res_ele, Results_ele,station_ele
from import_export.admin import ExportActionModelAdmin, ImportExportActionModelAdmin


# Register your models here.

@admin.register(elecontest)
class elecontestAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'enable', 'name', 'type', 'start_date', 'end_date']
    list_editable = ['name', 'enable', 'type']
    list_filter = ['enable', 'type']


@admin.register(station_ele)
class station_eleAdmin(ImportExportActionModelAdmin):
    list_display = ['id','name']

@admin.register(EleRecord)
class EleRecordAdmin(ExportActionModelAdmin):
    list_display = ['id', 'belong_ele', 'sid', 'file_open']
    list_filter = ['belong_ele', 'sid']
    list_display_links = ['belong_ele']


@admin.register(Choice_ele)
class Choice_eleAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'belong_ele', 'belong_question']
    list_filter = ['belong_ele']


@admin.register(Multiple_ele)
class Multiple_eleAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'belong_ele', 'belong_question']
    list_filter = ['belong_ele']


@admin.register(Judge_ele)
class Judge_eleAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'belong_ele', 'belong_question']
    list_filter = ['belong_ele']


@admin.register(Choice_res_ele)
class Choice_res_eleAdmin(ExportActionModelAdmin):
    list_display = ['id', 'belong_ele', 'sid', 'belong_question', 'isscore', 'score', 'answer']
    list_filter = ['belong_ele', 'sid']
    search_fields = ['belong_question']


@admin.register(Multiple_res_ele)
class Multiple_res_eleAdmin(ExportActionModelAdmin):
    list_display = ['id', 'belong_ele', 'sid', 'belong_question', 'isscore', 'score', 'answer']
    list_filter = ['belong_ele', 'sid']
    search_fields = ['belong_question']


@admin.register(Judge_res_ele)
class Judge_res_eleAdmin(ExportActionModelAdmin):
    list_display = ['id', 'belong_ele', 'sid', 'belong_question', 'isscore', 'score', 'answer']
    list_filter = ['belong_ele', 'sid']
    search_fields = ['belong_question']


@admin.register(Results_ele)
class Results_eleAdmin(ExportActionModelAdmin):
    list_display = ['id', 'belong_ele', 'sid', 'score', 'submit']
    list_filter = ['belong_ele', 'sid']
    search_fields = ['belong_question']
