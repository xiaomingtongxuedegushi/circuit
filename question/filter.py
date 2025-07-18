import django_filters
from question.models import Choice,Multiple_Choice,Judge

class ChoiceFilter(django_filters.rest_framework.FilterSet):
    # right_answer_fi = django_filters.DateFilter(field_name='right_answer',lookup_expr='')
    class Meta:
        model = Choice
        fields = ['belong_class','type','belong_type']

class Multiple_ChoiceFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = Multiple_Choice
        fields = ['belong_class','type','belong_type']

class JudgeFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = Judge
        fields = ['belong_class','type','belong_type']