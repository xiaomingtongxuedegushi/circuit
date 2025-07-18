import json

from django.db import transaction
from django.shortcuts import render
from electron.models import elecontest, EleRecord, Choice_ele, Multiple_ele, Judge_ele, Choice_res_ele, \
    Multiple_res_ele, Judge_res_ele, station_ele, Results_ele
from question.models import Choice, Multiple_Choice, Judge
from electron.serializers import elecontestSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone

# Create your views here.
# 获取电子竞赛
from usermanage.models import Students,Teachers


@api_view(['POST'])
def eleLogin(request):
    sid = request.POST['sid']
    st = request.POST['sta']
    tid = request.POST['tid']
    s = Students.objects.filter(sid=sid)
    sta = station_ele.objects.filter(name=st)
    t = Teachers.objects.filter(tid=tid)
    if len(s) > 0 and len(t) > 0:
        if len(sta) > 0:
            return Response('success')
        else:
            return Response('None')
    else:
        return Response('error')


@api_view(['GET'])
def getEle(request):
    ele = elecontest.objects.filter(enable=True).order_by('-id')
    if len(ele) > 0:
        choice = Choice_ele.objects.filter(belong_ele=ele[0])
        multiple = Multiple_ele.objects.filter(belong_ele=ele[0])
        judge = Judge_ele.objects.filter(belong_ele=ele[0])
        is_choice = True
        if len(choice) == 0 and len(multiple) == 0 and len(judge) == 0:
            is_choice = False
        data = {
            'id': ele[0].id,
            'name': ele[0].name,
            'enable': ele[0].enable,
            'type': ele[0].type,
            'start_date': timezone.localtime(ele[0].start_date).strftime("%Y-%m-%d %H:%M:%S"),
            'end_date': timezone.localtime(ele[0].end_date).strftime("%Y-%m-%d %H:%M:%S"),
            'fault': "[" + ele[0].fault + "]",
            'file': str(ele[0].file),
            'remarks':ele[0].remarks,
            'is_choice':is_choice
        }
        return Response(data)
    else:
        return Response('None')


@api_view(['GET'])
def getEleList(request):
    data = []
    ele = elecontest.objects.all()
    for e in ele:
        data_item = {
            'value': e.id,
            'label': e.name
        }
        data.append(data_item)
    return Response(data)


@api_view(['GET'])
def getEleinfo(request):
    eleid = request.GET['eleid']
    ele = elecontest.objects.filter(id=eleid).first()
    choice = Choice_ele.objects.filter(belong_ele=ele)
    multiple = Multiple_ele.objects.filter(belong_ele=ele)
    judge = Judge_ele.objects.filter(belong_ele=ele)
    data = {
        'name': ele.name,
        'enable': ele.enable,

        'choice': len(choice),
        'multiple': len(multiple),
        'judge': len(judge),
    }
    return Response(data)


@api_view(['POST'])
def addChoice_ele(request):
    chid = request.POST['chid']
    exam = request.POST['exam']
    print(chid, exam)
    try:
        choice = Choice.objects.filter(id=chid)
        ex = elecontest.objects.filter(id=exam)
        c = Choice_ele.objects.filter(belong_ele=ex[0], belong_question=choice[0])
        if len(c) > 0:
            return Response('error')
        else:
            ct = Choice_ele(belong_ele=ex[0], belong_question=choice[0])
            ct.save()
            return Response('ok')
    except:
        return Response('error')


@api_view(['POST'])
def addMutiple_ele(request):
    chid = request.POST['chid']
    exam = request.POST['exam']
    try:
        multiple = Multiple_Choice.objects.filter(id=chid)
        ex = elecontest.objects.filter(id=exam)
        c = Multiple_ele.objects.filter(belong_ele=ex[0], belong_question=multiple[0])
        if len(c) > 0:
            return Response('error')
        else:
            ct = Multiple_ele(belong_ele=ex[0], belong_question=multiple[0])
            ct.save()
            return Response('ok')
    except:
        return Response('error')


@api_view(['POST'])
def addJudge_ele(request):
    chid = request.POST['chid']
    exam = request.POST['exam']
    try:
        judge = Judge.objects.filter(id=chid)
        ex = elecontest.objects.filter(id=exam)
        c = Judge_ele.objects.filter(belong_ele=ex[0], belong_question=judge[0])
        if len(c) > 0:
            return Response('error')
        else:
            ct = Judge_ele(belong_ele=ex[0], belong_question=judge[0])
            ct.save()
            return Response('ok')
    except:
        return Response('error')


@api_view(['POST'])
def delChoice_ele(request):
    chid = request.POST['chid']
    exam = request.POST['exam']

    try:
        choice = Choice.objects.filter(id=chid)
        ex = elecontest.objects.filter(id=exam)
        de = Choice_ele.objects.filter(belong_ele=ex[0], belong_question=choice[0])
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
def delMutiple_ele(request):
    chid = request.POST['chid']
    exam = request.POST['exam']

    try:
        multiple = Multiple_Choice.objects.filter(id=chid)
        ex = elecontest.objects.filter(id=exam)
        de = Multiple_ele.objects.filter(belong_ele=ex[0], belong_question=multiple[0])
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
def delJudge_ele(request):
    chid = request.POST['chid']
    exam = request.POST['exam']

    try:
        judge = Judge.objects.filter(id=chid)
        ex = elecontest.objects.filter(id=exam)
        de = Judge_ele.objects.filter(belong_ele=ex[0], belong_question=judge[0])
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
def getElechoices(request):
    id = request.GET['id']
    ex = elecontest.objects.filter(id=id)
    if len(ex) > 0:
        data = []
        choice = Choice_ele.objects.filter(belong_ele=ex[0])
        for c in choice:
            # question = Choice.objects.filter(id=c.belong_question.id)
            # if len(question)>0:
            # print(c.belong_question.right_answer)
            data_item = {
                'id': c.belong_question.id,
                'question': c.belong_question.question,
                'answer_A': c.belong_question.answer_A,
                'answer_B': c.belong_question.answer_B,
                'answer_C': c.belong_question.answer_C,
                'answer_D': c.belong_question.answer_D,
                'image': str(c.belong_question.images),
                'type': 'choice'
            }
            data.append(data_item)
        multiple = Multiple_ele.objects.filter(belong_ele=ex[0])
        for c in multiple:
            # question = Multiple_Choice.objects.filter(id=c.id)
            # if len(question)>0:
            # print(c.belong_question.right_answer)
            data_item = {
                'id': c.belong_question.id,
                'question': c.belong_question.question,
                'answer_A': c.belong_question.answer_A,
                'answer_B': c.belong_question.answer_B,
                'answer_C': c.belong_question.answer_C,
                'answer_D': c.belong_question.answer_D,
                'image': str(c.belong_question.images),
                'type': 'multiple'
            }
            data.append(data_item)
        judge = Judge_ele.objects.filter(belong_ele=ex[0])
        for c in judge:
            # question = Judge.objects.filter(id=c.id)
            # if len(question)>0:
            # print(c.belong_question.right_answer)
            data_item = {
                'id': c.belong_question.id,
                'question': c.belong_question.question,
                'image': str(c.belong_question.images),
                'type': 'judge'
            }
            data.append(data_item)
        return Response(data)


# 提交竞赛成绩
@api_view(['POST'])
def post_ele_choice(request):
    ele_id = request.POST['ele_id']
    sid = request.POST['sid']
    score = request.POST['sc']
    num = request.POST.get('num')
    st = request.POST.get('sta')
    # print(num)
    ele = elecontest.objects.filter(id=ele_id)
    stu = Students.objects.filter(sid=sid)
    sta = station_ele.objects.filter(id=st).first()
    str1 = json.loads(score)

    # 保存批量添加数组
    print(str1)
    choice_score = []
    multiple_score = []
    judge_score = []
    # 竞赛评分
    score_type = ele[0].type
    total_score = 0
    # 实训评分
    num_trues = 0

    for c in str1[0]:
        iscore = False
        question = Choice.objects.filter(id=c['id'])
        if question[0].right_answer == c['answer']:
            iscore = True
        if score_type:
            if iscore:
                choice_score.append(
                    Choice_res_ele(belong_ele=ele[0], belong_question=question[0],
                                   isscore=iscore, answer=c['answer'], sid=stu[0], score=question[0].score))
                total_score = total_score + question[0].score
            else:
                choice_score.append(
                    Choice_res_ele(belong_ele=ele[0], belong_question=question[0],
                                   isscore=iscore, answer=c['answer'], sid=stu[0], score=0))
        else:
            choice_score.append(
                Choice_res_ele(belong_ele=ele[0], belong_question=question[0], isscore=iscore,
                               answer=c['answer'], sid=stu[0]))
            if iscore:
                num_trues += 1
    for c in str1[1]:
        iscore = False
        question = Multiple_Choice.objects.filter(id=c['id'])
        if str(list(question[0].right_answer)) == str(list(filter(None, c['answer']))):
            iscore = True
        # print(iscore)
        if score_type:
            if iscore:
                multiple_score.append(
                    Multiple_res_ele(belong_ele=ele[0], belong_question=question[0],
                                     isscore=iscore,
                                     answer=str(list(filter(None, c['answer']))).replace("'", "\"").replace(r"\n", ""),
                                     sid=stu[0], score=question[0].score))
                total_score = total_score + question[0].score
            else:
                multiple_score.append(
                    Multiple_res_ele(belong_ele=ele[0], belong_question=question[0],
                                     isscore=iscore,
                                     answer=str(list(filter(None, c['answer']))).replace("'", "\"").replace(r"\n", ""),
                                     sid=stu[0], score=0))
        else:
            multiple_score.append(
                Multiple_res_ele(belong_ele=ele[0], belong_question=question[0], isscore=iscore,
                                 answer=str(list(filter(None, c['answer']))).replace("'", "\"").replace(r"\n", ""),
                                 sid=stu[0]))
            if iscore:
                num_trues += 1
    for c in str1[2]:
        iscore = False
        question = Judge.objects.filter(id=c['id'])
        if question[0].right_answer == c['answer']:
            iscore = True
        if score_type:
            if iscore:
                judge_score.append(Judge_res_ele(belong_ele=ele[0], belong_question=question[0],
                                                 isscore=iscore, answer=c['answer'], sid=stu[0],
                                                 score=question[0].score))
                total_score = total_score + question[0].score
            else:
                judge_score.append(Judge_res_ele(belong_ele=ele[0], belong_question=question[0],
                                                 isscore=iscore, answer=c['answer'], sid=stu[0], score=0))
        else:
            judge_score.append(
                Judge_res_ele(belong_ele=ele[0], belong_question=question[0], isscore=iscore,
                              answer=c['answer'], sid=stu[0]))
            if iscore:
                num_trues += 1
    try:
        if score_type:
            pass
        else:
            total_score = 0
            total_score = format(float(format(float(num_trues) / float(num), '.2f')) * 100, '.2f')
            # print(sx_score)
        with transaction.atomic():
            print(choice_score)
            print(judge_score)
            if choice_score:
                ch = Choice_res_ele.objects.bulk_create(choice_score)
            if judge_score:
                ju = Judge_res_ele.objects.bulk_create(judge_score)
            if multiple_score:
                mu = Multiple_res_ele.objects.bulk_create(multiple_score)

            res = Results_ele(belong_ele=ele[0], sid=stu[0], score=total_score, belong_sta=sta)
            res.save()
            # print(time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime()))
            return Response('ok')
    except:
        return Response('error')


@api_view(['GET'])
def getScore(request):
    ele_id = request.GET['ele_id']
    sid = request.GET['sid']
    try:
        stu = Students.objects.filter(sid=sid).first()
        ele = elecontest.objects.filter(id=ele_id).first()
        res = Results_ele.objects.filter(belong_ele=ele, sid=stu)
        if len(res) == 0:
            return Response('None')
        else:
            choice = []
            data = {
                'id': ele.id,
                'name': ele.name,
                'score': res[0].score,
                'choice': choice,
            }
            ch_res = Choice_res_ele.objects.filter(belong_ele=ele, sid=stu)
            if len(ch_res) > 0:
                for ch in ch_res:
                    choice_item = {
                        'question_id': ch.belong_question.id,
                        'question': ch.belong_question.question,
                        'answer_A': ch.belong_question.answer_A,
                        'answer_B': ch.belong_question.answer_B,
                        'answer_C': ch.belong_question.answer_C,
                        'answer_D': ch.belong_question.answer_D,
                        'right_answer': ch.belong_question.right_answer,
                        'isscore': ch.isscore,
                        'score': ch.score,
                        'answer': ch.answer,
                        'type': 'choice',
                    }
                    choice.append(choice_item)
            mu_res = Multiple_res_ele.objects.filter(belong_ele=ele, sid=stu)
            if len(mu_res) > 0:
                for mu in mu_res:
                    multiple_item = {
                        'question_id': mu.belong_question.id,
                        'question': mu.belong_question.question,
                        'answer_A': mu.belong_question.answer_A,
                        'answer_B': mu.belong_question.answer_B,
                        'answer_C': mu.belong_question.answer_C,
                        'answer_D': mu.belong_question.answer_D,
                        'right_answer': mu.belong_question.right_answer,
                        'isscore': mu.isscore,
                        'score': mu.score,
                        'answer': mu.answer,
                        'type': 'multiple',
                    }
                    choice.append(multiple_item)

            ju_res = Judge_res_ele.objects.filter(belong_ele=ele, sid=stu)
            if len(ju_res) > 0:
                for ju in ju_res:
                    judge_item = {
                        'question_id': ju.belong_question.id,
                        'question': ju.belong_question.question,
                        'isscore': ju.isscore,
                        'score': ju.score,
                        'answer': ju.answer,
                        'type': 'judge',
                    }
                    choice.append(judge_item)
            return Response(data)
    except:
        return Response('error')


@api_view(['POST'])
def subFiles(request):
    ele_id = request.POST['ele_id']
    sid = request.POST['sid']
    file = request.FILES.get('file', None)
    try:
        ele = elecontest.objects.filter(id=ele_id).first()
        stu = Students.objects.filter(sid=sid).first()
        if not file:
            return Response('error')
        else:
            elerecord = EleRecord.objects.filter(belong_ele=ele, sid=stu)
            if len(elerecord) > 0:
                elerecord[0].file = file
                elerecord[0].save()
                return Response("ok")
            else:
                eler = EleRecord(belong_ele=ele, sid=stu, file=file)
                eler.save()
                return Response("ok")
    except:
        return Response("error")


@api_view(['GET'])
def checkEleScore(request):
    sid = request.GET['sid']
    ele_id = request.GET['ele_id']
    try:
        ele = elecontest.objects.filter(id=ele_id).first()
        stu = Students.objects.filter(sid=sid).first()
        res = Results_ele.objects.filter(belong_ele=ele,sid=stu)
        elerecord = EleRecord.objects.filter(belong_ele=ele, sid=stu)
        choice = False
        files = False
        if len(res) > 0:
            choice = True
        if len(elerecord) > 0:
            files = True
        data = {
            'id':ele.id,
            'name':ele.name,
            'choice':choice,
            'file':files,
        }
        return Response(data)
    except:
        return Response('error')


# @api_view(['GET'])
# def checkChoice(request):
#     ele_id = request.GET['ele_id']
#     try:
#         ele = elecontest.objects.filter(id=ele_id).first()
        
