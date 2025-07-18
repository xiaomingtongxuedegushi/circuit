from rest_framework.decorators import api_view
from rest_framework.response import Response
from data.models import Classification
from examination.models import Examinations
from question.models import Choice, Judge, Multiple_Choice,QuestionType
from question.serializers import ChoiceSerializer, JudgeSerializer, Multiple_choiceSerializer


@api_view(['GET'])
def get_choices(request):
    choices = Choice.objects.all()
    choices_data = ChoiceSerializer(choices, many=True)

    return Response(choices_data.data)


@api_view(['GET'])
def get_judges(request):
    judges = Judge.objects.all()
    judges_data = JudgeSerializer(judges, many=True)

    return Response(judges_data.data)


@api_view(['GET'])
def get_multiple_choice(request):
    multiple_choice = Multiple_Choice.objects.all()
    multiple_choices = Multiple_choiceSerializer(multiple_choice, many=True)
    return Response(multiple_choices.data)

@api_view(['GET'])
def get_QuestionType(request):
    data = []
    qutype = QuestionType.objects.all()
    for q in qutype:
        data_item={
            'value': q.id,
            'label': q.question_type,
        }
        data.append(data_item)
    return Response(data)


@api_view(['GET'])
def get_classification(request):
    data = []
    classif = Classification.objects.all()
    for q in classif:
        data_item={
            'value': q.id,
            'label': q.class_name,
        }
        data.append(data_item)
    return Response(data)


@api_view(['GET'])
def getExamList(request):
    data=[]
    exam = Examinations.objects.all()
    for ex in exam:
        data_item={
            'value': ex.id,
            'label': ex.name
        }
        data.append(data_item)
    return Response(data)
