from rest_framework import serializers, viewsets

from examination.models import Examinations, Choice_Topic, Multiple_Choice_Topic, Judge_Topic, Results


class ExaminationsSerializers(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Examinations
        fields = '__all__'


class Choice_TopicSerializers(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Choice_Topic
        fields = ['belong_question']


class Multiple_Choice_TopicSerializers(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Multiple_Choice_Topic
        fields = ['belong_question']


class Judge_TopicSerializers(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Judge_Topic
        fields = ['belong_question']


class ResultsSerializers(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Results
        fields = ['sid', 'score', 'submit']
