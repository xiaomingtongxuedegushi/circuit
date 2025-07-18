from django.contrib import admin
from contest.models import Choice_job, Multiple_job, contestList, Modula, project, step, job, job_item, jobScore, \
    jobTotal, station, Record, Row, Column, Criteria, Choice_job, Multiple_job, Judge_job, Choice_res, Multiple_res, \
    Judge_res, Results_job, TableRecord, TableJobScore, Merge
from import_export.admin import ExportActionModelAdmin, ImportExportActionModelAdmin, ImportMixin


# Register your models here.
@admin.register(contestList)
class contestListAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'enable', 'disorder', 'name', 'type', 'start_date', 'end_date']
    list_editable = ['name', 'enable']


@admin.register(Modula)
class ModulaAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'name', 'belong_contest']
    list_editable = ['name', 'belong_contest']
    list_filter = ['belong_contest']
    search_fields = ['name']


@admin.register(project)
class projectAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'name', 'belong_modula']
    list_editable = ['name', 'belong_modula']
    list_filter = ['belong_modula']
    search_fields = ['name']


@admin.register(step)
class stepAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'name', 'tools', 'images', 'programme', 'attention', 'belong_project']
    list_editable = ['name', 'belong_project']
    list_filter = ['name', 'belong_project']
    search_fields = ['name']


@admin.register(job)
class JobAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'contest', 'name', 'description']
    list_editable = ['contest', 'name']


@admin.register(job_item)
class JobItemAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'name', 'score']


@admin.register(jobScore)
class JobScoreAdmin(ExportActionModelAdmin):
    list_display = ['id', 'belong_contestList', 'studen', 'belong_st', 'belong_job', 'belong_job_item', 'score',
                    'teacher']
    list_filter = ['belong_contestList', 'studen', 'teacher']
    search_fields = ['belong_job']


@admin.register(jobTotal)
class JobTotalAdmin(ExportActionModelAdmin):
    list_display = ['id', 'belong_contestList', 'studen', 'belong_st', 'score', 'teacher', 'submit', 'alter_time']
    list_filter = ['belong_contestList', 'studen', 'teacher']


@admin.register(station)
class StationAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'name']


@admin.register(Record)
class RecordAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'belong_job', 'table', 'column_header', 'row_header']


@admin.register(Row)
class RowAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'table', 'row_name']


@admin.register(Column)
class ColumnAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'table', 'column_name']


@admin.register(Criteria)
class CriteriaAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'table', 'row', 'column', 'answer', 'error', 'type']
    list_editable = ['error']


@admin.register(Choice_job)
class ChoiceJobAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'belong_job', 'belong_question']
    search_fields = ['belong_question']
    list_filter = ['belong_job']


@admin.register(Multiple_job)
class MultipleJobAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'belong_job', 'belong_question']
    search_fields = ['belong_question']
    list_filter = ['belong_job']


@admin.register(Judge_job)
class JudgeJobAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'belong_job', 'belong_question']
    search_fields = ['belong_question']
    list_filter = ['belong_job']


@admin.register(Choice_res)
class Judge_resAdmin(ExportActionModelAdmin):
    list_display = ['id', 'belong_contestList', 'belong_job', 'sid', 'belong_question', 'isscore', 'score', 'answer']
    list_filter = ['belong_contestList', 'belong_job', 'sid']
    search_fields = ['belong_question']


@admin.register(Multiple_res)
class Multiple_resAdmin(ExportActionModelAdmin):
    list_display = ['id', 'belong_contestList', 'belong_job', 'sid', 'belong_question', 'isscore', 'score', 'answer']
    list_filter = ['belong_contestList', 'belong_job', 'sid']
    search_fields = ['belong_question']


@admin.register(Judge_res)
class Judge_resAdmin(ExportActionModelAdmin):
    list_display = ['id', 'belong_contestList', 'belong_job', 'sid', 'belong_question', 'isscore', 'score', 'answer']
    list_filter = ['belong_contestList', 'belong_job', 'sid']
    search_fields = ['belong_question']


@admin.register(Results_job)
class Results_jobAdmin(ExportActionModelAdmin):
    list_display = ['id', 'belong_contestList', 'belong_job', 'sid', 'score', 'submit']
    list_filter = ['belong_contestList', 'belong_job', 'sid']
    search_fields = ['belong_question']


@admin.register(TableRecord)
class TableRecordAdmin(ExportActionModelAdmin):
    list_display = ['id', 'belong_contestList', 'belong_job', 'sid', 'table', 'row', 'column', 'answer', 'judge_answer',
                    'isscore', 'score']
    list_display_links = ['belong_contestList']
    list_filter = ['sid', 'table', 'belong_job']


@admin.register(TableJobScore)
class TableJobScoreAdmin(ExportActionModelAdmin):
    list_display = ['id', 'belong_contestList', 'belong_job', 'sid', 'score', 'submit']
    list_filter = ['sid', 'belong_job', 'belong_contestList']


@admin.register(Merge)
class MergeAdmin(ExportActionModelAdmin):
    list_display = ['id', 'belong_contestList', 'sid', 'score', 'teacher', 'submit', 'type']
    list_filter = ['belong_contestList', 'sid', 'teacher', 'type']
