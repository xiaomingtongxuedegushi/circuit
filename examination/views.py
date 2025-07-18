import datetime

from django.shortcuts import render
from django.utils import timezone

from examination.models import Examinations, Choice_Topic, Multiple_Choice_Topic, Judge_Topic, Results
from usermanage.models import Classes, Students
from question.models import Choice, Multiple_Choice, Judge
from rest_framework import mixins, viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from examination.serializers import ExaminationsSerializers, Multiple_Choice_TopicSerializers, Choice_TopicSerializers, \
    Judge_TopicSerializers, ResultsSerializers
from rest_framework.decorators import api_view


# Create your views here.


class ExadminationsListViewSet(ModelViewSet):
    queryset = Examinations.objects.all()
    serializer_class = ExaminationsSerializers


@api_view(['GET', 'POST'])
def getexamin(request):
    if request.method == 'GET':
        cl = request.GET['class']
        classes = Classes.objects.filter(id=cl)
        # now = timezone.now()
        # examin = Examinations.objects.filter(group=classes[0], enable=True, end_date__gt=now)
        examin = Examinations.objects.filter(group=classes[0], enable=True)
        examin_data = ExaminationsSerializers(examin, many=True)
        return Response(examin_data.data)


@api_view(['GET', 'POST'])
def getchoice_topic(request):
    if request.method == 'GET':
        exid = request.GET['id']
        ex = Examinations.objects.filter(id=exid)
        if ex[0].disorder:
            choice = Choice_Topic.objects.filter(belong_name=ex[0]).order_by('?')
        else:
            choice = Choice_Topic.objects.filter(belong_name=ex[0])
        choice_data = Choice_TopicSerializers(choice, many=True)
        return Response(choice_data.data)


@api_view(['GET', 'POST'])
def getMultiple_Choice_Topic(request):
    if request.method == 'GET':
        exid = request.GET['id']
        ex = Examinations.objects.filter(id=exid)
        multiple = Multiple_Choice_Topic.objects.filter(belong_name=ex[0])
        Multiple_Choice_Topic_data = Multiple_Choice_TopicSerializers(multiple, many=True)
        return Response(Multiple_Choice_Topic_data.data)


@api_view(['GET', 'POST'])
def getJudge_Topic(request):
    if request.method == 'GET':
        exid = request.GET['id']
        ex = Examinations.objects.filter(id=exid)
        judge = Judge_Topic.objects.filter(belong_name=ex[0])
        judge_data = Judge_TopicSerializers(judge, many=True)
        return Response(judge_data.data)


@api_view(['POST'])
def subGrades(request):
    exid = request.POST['exid']
    sid = request.POST['sid']
    score = request.POST['score']
    ex = Examinations.objects.filter(id=exid)
    stu = Students.objects.filter(sid=sid)
    d0 = ex[0].end_date
    d1 = timezone.now()
    if d0 < d1:
        return Response('date')
    else:
        try:
            same = Results.objects.filter(name=ex[0], sid=stu[0])
            # print(same)
            # print(len(same))
            if len(same) == 0:
                re = Results(name=ex[0], sid=stu[0], score=score)
                re.save()
                return Response('ok')
            else:
                return Response('same')
        except:
            return Response('error')


@api_view(['GET'])
def getGrades(request):
    exid = request.GET['exid']
    ex = Examinations.objects.filter(id=exid)
    re = Results.objects.filter(name=ex[0]).order_by('-score')
    data = []
    if len(re) == 0:
        return Response(data)
    else:
        for index, i in enumerate(re):
            data_item = {
                'index': index + 1,
                'name': i.sid.name,
                'score': i.score,
                'date': timezone.localtime(i.submit).strftime("%Y-%m-%d %H:%M:%S")
            }
            data.append(data_item)
        # re_data = ResultsSerializers(re, many=True)
        return Response(data)


@api_view(['POST'])
def addChoice(request):
    chid = request.POST['chid']
    exam = request.POST['exam']
    print(chid, exam)
    try:
        choice = Choice.objects.filter(id=chid)
        ex = Examinations.objects.filter(id=exam)
        c = Choice_Topic.objects.filter(belong_name=ex[0], belong_question=choice[0])
        if len(c) > 0:
            return Response('error')
        else:
            ct = Choice_Topic(belong_name=ex[0], belong_question=choice[0])
            ct.save()
            return Response('ok')
    except:
        return Response('error')


@api_view(['POST'])
def addMutiple(request):
    chid = request.POST['chid']
    exam = request.POST['exam']
    try:
        multiple = Multiple_Choice.objects.filter(id=chid)
        ex = Examinations.objects.filter(id=exam)
        c = Multiple_Choice_Topic.objects.filter(belong_name=ex[0], belong_question=multiple[0])
        if len(c) > 0:
            return Response('error')
        else:
            ct = Multiple_Choice_Topic(belong_name=ex[0], belong_question=multiple[0])
            ct.save()
            return Response('ok')
    except:
        return Response('error')


@api_view(['POST'])
def addJudge(request):
    chid = request.POST['chid']
    exam = request.POST['exam']
    try:
        judge = Judge.objects.filter(id=chid)
        ex = Examinations.objects.filter(id=exam)
        c = Judge_Topic.objects.filter(belong_name=ex[0], belong_question=judge[0])
        if len(c) > 0:
            return Response('error')
        else:
            ct = Judge_Topic(belong_name=ex[0], belong_question=judge[0])
            ct.save()
            return Response('ok')
    except:
        return Response('error')


@api_view(['POST'])
def delChoice(request):
    chid = request.POST['chid']
    exam = request.POST['exam']

    try:
        choice = Choice.objects.filter(id=chid)
        ex = Examinations.objects.filter(id=exam)
        de = Choice_Topic.objects.filter(belong_name=ex[0], belong_question=choice[0])
        if len(de) == 0:
            return Response('None')
        else:
            try:
                de.delete()
                return Response('ok')
            except:
                return Response('error')
    except:
        return Response('error')


@api_view(['POST'])
def delMutiple(request):
    chid = request.POST['chid']
    exam = request.POST['exam']

    try:
        multiple = Multiple_Choice.objects.filter(id=chid)
        ex = Examinations.objects.filter(id=exam)
        de = Multiple_Choice_Topic.objects.filter(belong_name=ex[0], belong_question=multiple[0])
        if len(de) == 0:
            return Response('None')
        else:
            try:
                de.delete()
                return Response('ok')
            except:
                return Response('error')
    except:
        return Response('error')


@api_view(['POST'])
def delJudge(request):
    chid = request.POST['chid']
    exam = request.POST['exam']

    try:
        judge = Judge.objects.filter(id=chid)
        ex = Examinations.objects.filter(id=exam)
        de = Judge_Topic.objects.filter(belong_name=ex[0], belong_question=judge[0])
        if len(de) == 0:
            return Response('None')
        else:
            try:
                de.delete()
                return Response('ok')
            except:
                return Response('error')
    except:
        return Response('error')


@api_view(['GET'])
def getexInfo(request):
    exid = request.GET['exid']
    ex = Examinations.objects.filter(id=exid)
    choice = Choice_Topic.objects.filter(belong_name=ex[0])
    multiple = Multiple_Choice_Topic.objects.filter(belong_name=ex[0])
    judge = Judge_Topic.objects.filter(belong_name=ex[0])
    data = {
        'name': ex[0].name,
        'enable': ex[0].enable,

        'choice': len(choice),
        'multiple': len(multiple),
        'judge': len(judge),
    }
    return Response(data)
