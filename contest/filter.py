import django_filters
from contest.models import TableRecord

class TableRecordFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = TableRecord
        fields =['belong_contestList','belong_job','sid','table']