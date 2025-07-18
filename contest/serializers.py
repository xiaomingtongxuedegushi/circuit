from rest_framework import serializers
from contest.models import step, job, Criteria, TableRecord


class StepSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 3
        model = step
        fields = '__all__'


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = job
        fields = '__all__'


class CriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Criteria
        fields = '__all__'


class TableRecordSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = TableRecord
        fields = '__all__'
