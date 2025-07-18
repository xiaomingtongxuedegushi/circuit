from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets,filters
from rest_framework.response import Response
from rest_framework.views import APIView
from question.filter import ChoiceFilter,Multiple_ChoiceFilter,JudgeFilter
from rest_framework.pagination import PageNumberPagination
from question.models import Choice,Multiple_Choice,Judge

from question.serializers import ChoiceSerializer,Multiple_choiceSerializer,JudgeSerializer


# Create your views here.

class CommonPagination(PageNumberPagination):
    """考试列表自定义分页"""
    # 默认每页显示的个数
    page_size = 10
    # 可以动态改变每页显示的个数
    page_size_query_param = 'page_size'
    # 页码参数
    page_query_param = 'page'
    # 最多能显示多少页
    max_page_size = 10


class ChoiceListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """选择题列表页"""
    # 这里要定义一个默认的排序，否则会报错
    queryset = Choice.objects.all().order_by('id')[:0]

    # 序列化
    serializer_class = ChoiceSerializer
    pagination_class = CommonPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ['question']
    # filter_backends =['question']
    filter_class=ChoiceFilter
    ordering_fields = ['id', 'type']
    # 重写queryset
    def get_queryset(self):
        # 题目数量
        # choice_number = int(self.request.query_params.get("choice_number"))
        # level = int(self.request.query_params.get("level", 1))

        self.queryset = Choice.objects.all()
        return self.queryset

class MultipleViewsView(mixins.ListModelMixin, viewsets.GenericViewSet):

    queryset=Multiple_Choice.objects.all().order_by('id')[:0]
    serializer_class=Multiple_choiceSerializer
    pagination_class = CommonPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ['question']
    ordering_fields = ['id', 'type']
    filter_class= Multiple_ChoiceFilter
    def get_queryset(self):
        self.queryset = Multiple_Choice.objects.all()
        return self.queryset

class JudgeViewsView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset=Judge.objects.all().order_by('id')[:0]
    serializer_class=JudgeSerializer
    pagination_class=CommonPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ['question']
    ordering_fields = ['id', 'type']
    filter_class = JudgeFilter
    def get_queryset(self):
        self.queryset = Judge.objects.all()
        return self.queryset
