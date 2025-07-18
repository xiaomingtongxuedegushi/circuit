from rest_framework import serializers

from question.models import Choice, Judge, Multiple_Choice


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Choice
        fields = '__all__'


class JudgeSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Judge
        fields = '__all__'


class Multiple_choiceSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Multiple_Choice
        fields = '__all__'
