from contest.models import TableRecord
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, filters
from contest.serializers import TableRecordSerializer
from contest.filter import TableRecordFilter
from data.models import serial


class CommonPagination(PageNumberPagination):
    """自定义分页"""
    # 默认每页显示的个数
    page_size = 10
    # 可以动态改变每页显示的个数
    page_size_query_param = 'page_size'
    # 页码参数
    page_query_param = 'page'
    # 最多能显示多少页
    max_page_size = 10


class TableRecordListViewSet(viewsets.ModelViewSet):
    queryset = TableRecord.objects.all().order_by('id')[:0]
    serializer_class = TableRecordSerializer
    pagination_class = CommonPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # serial_fields = ['']
    filter_class = TableRecordFilter
    ordering_fields = ['id', 'score']

    def get_queryset(self):
        # 题目数量
        # choice_number = int(self.request.query_params.get("choice_number"))
        # level = int(self.request.query_params.get("level", 1))

        self.queryset = TableRecord.objects.all()
        return self.queryset
