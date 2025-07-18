from usermanage.models import Students
import import_export.admin
from django.contrib import admin
from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget
from examination.models import Examinations, Choice_Topic, Multiple_Choice_Topic, Judge_Topic, Results
from import_export.admin import ExportActionModelAdmin, ImportExportModelAdmin, ImportExportActionModelAdmin, ExportMixin, ImportMixin
from simpleui.admin import AjaxAdmin



# Register your models here.


class JudgeResource(resources.ModelResource):
    # belong_name = Field(attribute='belong_name', column_name='试卷名称')
    # belong_question = Field(attribute='belong_question', column_name='问题')
    class Meta:
        model = Judge_Topic
        fields = ('belong_name', 'belong_question')

@admin.register(Examinations)
class Examinations(admin.ModelAdmin):
    list_display = ['name', 'enable', 'show', 'disorder', 'start_date', 'end_date', 'group', 'belong_te', 'remarks']
    search_fields = ['name']
    list_editable = ['enable', 'show', 'disorder']
    list_filter = ['group', 'belong_te']


@admin.register(Choice_Topic)
class Choice_TopicAdmin(ImportMixin, admin.ModelAdmin):
    list_display = ['id', 'belong_name', 'belong_question']
    list_filter = ['belong_name']
    # filter_horizontal = ['belong_question']
    list_display_links = ['id', 'belong_name']
    autocomplete_fields = ['belong_question']
    search_fields = ['belong_question']
    # resource_class=JudgeResource

@admin.register(Multiple_Choice_Topic)
class Multiple_Choice_TopicAdmin(ImportMixin, admin.ModelAdmin):
    list_display = ['id', 'belong_name', 'belong_question']
    list_filter = ['belong_name']
    list_display_links = ['id', 'belong_name']
    autocomplete_fields = ['belong_question']
    search_fields = ['belong_question']
    # resource_class=JudgeResource


@admin.register(Judge_Topic)
class Judge_TopicAdmin(ImportMixin, admin.ModelAdmin):
    list_display = ['id', 'belong_name', 'belong_question']
    list_filter = ['belong_name']
    list_display_links = ['id', 'belong_name']
    autocomplete_fields = ['belong_question']
    search_fields = ['belong_question']
    # resource_class=JudgeResource


class ResultsResource(resources.ModelResource):
    id = Field(attribute='id', column_name='ID')
    name = Field(attribute='name', column_name='试卷名称',widget=ForeignKeyWidget(Examinations,'name'))
    sid = Field(attribute='sid', column_name='姓名',widget=ForeignKeyWidget(Students,'name'))
    score = Field(attribute='score', column_name='分数')
    submit = Field(attribute='submit', column_name='提交时间')

    class Meta:
        model = Results 
        fields = ('id','name', 'sid', 'score', 'submit')
        export_order = ('id', 'name', 'sid', 'score', 'submit')


@admin.register(Results)
class ResultsAdmin(ExportActionModelAdmin, admin.ModelAdmin):
    list_display = ['name', 'sid', 'score', 'submit']
    list_filter = ['name']
    list_display_links = ['name', 'sid']
    search_fields = ['sid']
    list_editable = ['score']
    resource_class = ResultsResource
