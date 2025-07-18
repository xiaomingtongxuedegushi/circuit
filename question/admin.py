from examination.admin import JudgeResource
from django.contrib import admin
from question.models import Choice, Judge, Multiple_Choice, QuestionType
from import_export.admin import ImportExportMixin, ImportExportModelAdmin, ImportExportActionModelAdmin
from django.db.models import Q
from import_export import resources
from import_export.fields import Field


# Register your models here.

# class ChoiceResource(resources.ModelResource):
    
#     # question = Field(attribute='question',column_name='问题')
#     # answer_A = Field(attribute='answer_A',column_name='A选项')
#     # answer_B = Field(attribute='answer_B',column_name='B选项')
#     # answer_C = Field(attribute='answer_C',column_name='C选项')
#     # answer_D = Field(attribute='answer_D',column_name='D选项')
#     # right_answer = Field(attribute='right_answer',column_name='正确选项')
#     # level = Field(attribute='level',column_name='难度等级')
#     # belong_class = Field(attribute='belong_class',column_name='车型')
#     # belong_type = Field(attribute='belong_type',column_name='题目类型')
#     # remarks = Field(attribute='remarks',column_name='备注')
    
#     class Meta:
#         models = Choice
#         # fields = ('id','question','answer_A','answer_B','answer_C','answer_D','right_answer','level','belong_class', 'belong_type','remarks')
#         # skip_unchanged = True
#         # # 导入数据时，如果该条数据未修改过，则会忽略
#         # report_skipped = True
#         # # 在导入预览页面中显示跳过的记录
#         exclude = ['id','type']
#         # import_id_fields = ('id',)
#         # 对象标识的默认字段是id，您可以选择在导入时设置哪些字段用作id
       

class ChoiceResource(resources.ModelResource):

    class Meta:
        model = Choice
        exclude =['type']
        

@admin.register(Choice)
class ChoiceAdmin(ImportExportActionModelAdmin,admin.ModelAdmin):
    list_display = ['id', 'question', 'right_answer', 'level', 'belong_class', 'belong_type', 'remarks']
    list_display_links = ['id', 'question']
    search_fields = ['id', 'question']
    list_filter = ['belong_class', 'belong_type']
    list_per_page = 20
    resource_class=ChoiceResource
    # resource_class = ChoiceResource

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
    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     kwargs['queryset'] = QuestionType.objects.filter(id__lt=2)
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)

class JudgeResource(resources.ModelResource):

    class Meta:
        model = Judge
        exclude =['type']

    # question = Field(attribute='question',column_name='问题')
    # right_answer = Field(attribute='right_answer',column_name='正确选项')
    # level = Field(attribute='level',column_name='难度等级')
    # belong_class = Field(attribute='belong_class',column_name='车型')
    # belong_type = Field(attribute='belong_type',column_name='题目类型')
    # remarks = Field(attribute='remarks',column_name='备注')


@admin.register(Judge)
class JudgeAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'question', 'right_answer', 'level', 'belong_class', 'belong_type', 'remarks']
    list_display_links = ['id', 'question']
    search_fields = ['id', 'question']
    list_filter = ['belong_class', 'belong_type']
    list_per_page = 20
    resource_class = JudgeResource

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

class Multiple_ChoiceResorce(resources.ModelResource):
    class Meta:
        model = Multiple_Choice
        exclude =['type']



@admin.register(Multiple_Choice)
class Multiple_Choice(ImportExportActionModelAdmin):
    list_display = ['id', 'question', 'right_answer', 'level', 'belong_class', 'belong_type', 'remarks']
    list_display_links = ['id', 'question']
    search_fields = ['id', 'question']
    list_filter = ['belong_class', 'belong_type']
    list_per_page = 20
    resource_class=Multiple_ChoiceResorce
    # resource_class= ChoiceResource

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


@admin.register(QuestionType)
class QuestionTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'question_type']
