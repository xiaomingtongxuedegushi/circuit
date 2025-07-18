from django.shortcuts import render
import json, time, base64, os
from django.utils import timezone
from circuit.settings import MEDIA_ROOT
from usermanage.models import Teachers, Students
from contest.models import Choice_job, Choice_res, Judge_job, Judge_res, Multiple_job, Multiple_res, Record, \
    Results_job, jobScore, jobTotal, station, step, contestList, Modula, project, job, job_item, station, Criteria, Row, \
    Column, TableRecord, TableJobScore, Merge
from rest_framework.response import Response
from rest_framework.decorators import api_view
from question.models import Choice, Multiple_Choice, Judge
from contest.serializers import StepSerializer, JobSerializer, CriteriaSerializer
from django.db import transaction


# Create your views here.


@api_view(['GET'])
def set_point(request):
    return Response("ok")

@api_view(['POST'])
def testlogin(request):
    sid = request.POST['sid']
    st = request.POST['sta']
    tid = request.POST['tid']
    s = Students.objects.filter(sid=sid)
    sta = station.objects.filter(name=st)
    t = Teachers.objects.filter(tid=tid)
    if len(s) > 0 and len(t) > 0:
        if len(sta) > 0:
            return Response('success')
        else:
            return Response('None')
    else:
        return Response('error')


@api_view(['GET'])
def get_step(request):
    contest = request.GET['id']
    # type = request.GET['type']
    modu = Modula.objects.filter(belong_contest=contest)

    # st = step.objects.all()
    # st_data = StepSerializer(st,many=True)
    data = []
    for c in modu:
        pro = project.objects.filter(belong_modula=c)
        for p in pro:
            st = step.objects.filter(belong_project=p)
            for s in st:
                data_item = {
                    'modu': c.name,
                    'pro': p.name,
                    'name': s.name,
                    'programme': s.programme,
                    'images': str(s.images),
                    'tools': s.tools,
                    'attention': s.attention,
                }
                data.append(data_item)
    return Response(data)


@api_view(['GET'])
def getContest(request):
    contest = contestList.objects.filter(enable=True).order_by('-id')
    if len(contest) > 0:
        data = {
            'id': contest[0].id,
            'name': contest[0].name,
            'disorder': contest[0].disorder,
            'type': contest[0].type,
            'start_date': timezone.localtime(contest[0].start_date).strftime("%Y-%m-%d %H:%M:%S"),
            'end_date': timezone.localtime(contest[0].end_date).strftime("%Y-%m-%d %H:%M:%S"),
            'image': str(contest[0].images),
            'pdfs': str(contest[0].pdfs),
        }
        return Response(data)
    else:
        return Response('error')


@api_view(['GET'])
def get_job(request):
    contest = request.GET['id']
    data = []
    jobs = job.objects.filter(contest=contest)
    for j in jobs:
        datas = []
        jt = job_item.objects.filter(belong_job=j)
        for i in jt:
            data_item = {
                'jobid': j.id,
                'job': j.name,
                'id': i.id,
                'item': i.name,
                'score': i.score
            }
            datas.append(data_item)
        data.append(datas)
    return Response(data)


# 提交作业总分（批量添加）
@api_view(['POST'])
def subJobscore(request):
    sid = request.POST['sid']
    tid = request.POST['tid']
    st = request.POST['sta']
    # print(st)
    con = request.POST['con']
    item = request.POST['item']
    str1 = json.loads(item)
    # print(sid, tid, item)
    source = []
    sta = station.objects.filter(name=st)
    stu = Students.objects.filter(sid=sid)
    t = Teachers.objects.filter(tid=tid)
    c = contestList.objects.filter(id=con)
    # print(str1[0])

    for s in str1:
        if s:
            for i in s:
                if i:
                    jobs = job.objects.filter(id=i['jobid'])
                    it = job_item.objects.filter(id=i['id'])
                    source.append(jobScore(belong_contestList=c[0], belong_st=sta[0], studen=stu[0], teacher=t[0],
                                           belong_job=jobs[0], belong_job_item=it[0], score=i['score']))
    try:
        j = jobScore.objects.bulk_create(source)
        # print(source)
        return Response('ok')
    except:
        return Response('error')


@api_view(['GET'])
def getjobTotal(request):
    sid = request.GET['sid']
    con = request.GET['con']
    tid = request.GET['tid']
    s = Students.objects.filter(sid=sid)
    t = Teachers.objects.filter(tid=tid)
    c = contestList.objects.filter(id=con, enable=True).order_by('-id')
    if len(s) > 0 and len(t) > 0:
        jt = jobTotal.objects.filter(belong_contestList=c[0], studen=s[0], teacher_id=tid)
        if len(jt) > 0:
            # 已存在成绩，且不存在签名，则可再次登录
            if jt[0].images == '':
                return Response('None')
            else:
                data = {
                    'sid': jt[0].studen.sid,
                    'score': jt[0].score,
                }
                return Response(data)
        else:
            return Response('None')
    else:
        return Response('error')


@api_view(['POST'])
def postTotal(request):
    sid = request.POST['sid']
    con = request.POST['con']
    tid = request.POST['tid']
    score = request.POST['score']
    st = request.POST['sta']
    # 是否为在登录页提交
    isStart = request.POST['isStart']
    s = Students.objects.filter(sid=sid)
    c = contestList.objects.filter(id=con, enable=True)
    if len(c) > 0:
        t = Teachers.objects.filter(tid=tid)
        sta = station.objects.filter(name=st)
        if len(sta) > 0:
            jt = jobTotal.objects.filter(belong_contestList=c[0], studen=s[0], teacher_id=tid)

            if len(jt) > 0:
                if isStart == 'yes':
                    if jt[0].images == '':
                        return Response('error2')
                    else:
                        return Response('error')
                else:
                    if jt[0].score == 0.0:
                        # print(request.FILES)
                        base64Imag = request.POST['img']
                        image = base64Imag.split(",")
                        result = image[1]
                        image_data = base64.b64decode(result)
                        image_name = 'jobTotal/%s.jpg' % int(time.strftime("%Y%m%d%H%M%S"))
                        image_url = os.path.join(MEDIA_ROOT, image_name).replace('\\', '/')
                        with open(image_url, 'wb') as f:
                            f.write(image_data)
                        jts = jobTotal.objects.get(belong_contestList=c[0], studen=s[0], teacher_id=tid)
                        jts.score = score
                        jts.images = image_name
                        jts.save()
                        return Response('save')
                    else:
                        return Response('error')
            else:
                jtotal = jobTotal(belong_contestList=c[0], studen=s[0], belong_st=sta[0], score=score, teacher=t[0])
                jtotal.save()
                return Response('ok')
        else:
            return Response('error')
    else:
        return Response('error')


# 列表

@api_view(['GET'])
def getCriteria(request):
    tab = request.GET['tab']
    cri = Criteria.objects.filter(table=tab)
    cr_data = CriteriaSerializer(cri, many=True)
    return Response(cr_data.data)


# 理论考核

@api_view(['GET'])
def get_job_model(request):
    con = contestList.objects.all()
    data = []
    if len(con) > 0:
        for c in con:
            children = []
            data_item = {
                'value': c.id,
                'label': c.name,
                'children': children,
            }
            jobs = job.objects.filter(contest=c)
            if len(jobs) > 0:
                for j in jobs:
                    data_jobs = {
                        'value': j.id,
                        'label': j.name,
                    }
                    children.append(data_jobs)
            data.append(data_item)
        return Response(data)


@api_view(['GET'])
def get_exam_len(request):
    id = request.GET['id']
    jobs = job.objects.filter(id=id)
    choice = Choice_job.objects.filter(belong_job=jobs[0])
    multiple = Multiple_job.objects.filter(belong_job=jobs[0])
    judge = Judge_job.objects.filter(belong_job=jobs[0])

    data = {
        'name': jobs[0].name,
        'choice': len(choice),
        'multiple': len(multiple),
        'judge': len(judge),
    }
    return Response(data)


@api_view(['POST'])
def addChoice_job(request):
    chid = request.POST['chid']
    jobid = request.POST['jobid']
    # print(chid, exam)
    try:
        choice = Choice.objects.filter(id=chid)
        j = job.objects.filter(id=jobid)
        c = Choice_job.objects.filter(belong_job=j[0], belong_question=choice[0])
        if len(c) > 0:
            return Response('error')
        else:
            ct = Choice_job(belong_job=j[0], belong_question=choice[0])
            ct.save()
            return Response('ok')
    except:
        return Response('error')


@api_view(['POST'])
def addMutiple_job(request):
    chid = request.POST['chid']
    jobid = request.POST['jobid']
    try:
        multiple = Multiple_Choice.objects.filter(id=chid)
        j = job.objects.filter(id=jobid)
        c = Multiple_job.objects.filter(belong_job=j[0], belong_question=multiple[0])
        if len(c) > 0:
            return Response('error')
        else:
            ct = Multiple_job(belong_job=j[0], belong_question=multiple[0])
            ct.save()
            return Response('ok')
    except:
        return Response('error')


@api_view(['POST'])
def addJudge_job(request):
    chid = request.POST['chid']
    jobid = request.POST['jobid']
    try:
        judge = Judge.objects.filter(id=chid)
        j = job.objects.filter(id=jobid)
        c = Judge_job.objects.filter(belong_job=j[0], belong_question=judge[0])
        if len(c) > 0:
            return Response('error')
        else:
            ct = Judge_job(belong_job=j[0], belong_question=judge[0])
            ct.save()
            return Response('ok')
    except:
        return Response('error')


@api_view(['POST'])
def delChoice_job(request):
    chid = request.POST['chid']
    jobid = request.POST['jobid']

    try:
        choice = Choice.objects.filter(id=chid)
        j = job.objects.filter(id=jobid)
        de = Choice_job.objects.filter(belong_job=j[0], belong_question=choice[0])
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
def delMutiple_job(request):
    chid = request.POST['chid']
    jobid = request.POST['jobid']

    try:
        multiple = Multiple_Choice.objects.filter(id=chid)
        j = job.objects.filter(id=jobid)
        de = Multiple_job.objects.filter(belong_job=j[0], belong_question=multiple[0])
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
def delJudge_job(request):
    chid = request.POST['chid']
    jobid = request.POST['jobid']

    try:
        judge = Judge.objects.filter(id=chid)
        j = job.objects.filter(id=jobid)
        de = Judge_job.objects.filter(belong_job=j[0], belong_question=judge[0])
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
def getjobchoices(request):
    id = request.GET['id']
    jobs = job.objects.filter(id=id)
    if len(jobs) > 0:
        data = []
        choice = Choice_job.objects.filter(belong_job=jobs[0])
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
        multiple = Multiple_job.objects.filter(belong_job=jobs[0])
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
        judge = Judge_job.objects.filter(belong_job=jobs[0])
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


# 判断是否已有成绩
@api_view(['GET'])
def get_job_isscore(request):
    con_id = request.GET['con_id']
    job_id = request.GET['job_id']
    sid = request.GET['sid']
    con = contestList.objects.filter(id=con_id)
    jobs = job.objects.filter(id=job_id)
    stu = Students.objects.filter(sid=sid)
    try:
        re = Results_job.objects.filter(belong_contestList=con[0], belong_job=jobs[0], sid=stu[0])
        if len(re) > 0:
            return Response('same')
        else:
            return Response('None')
    except:
        return Response('error')


# 提交竞赛成绩
@api_view(['POST'])
def post_job_choice(request):
    # print(request.POST)
    # print(time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime()))
    con_id = request.POST['con_id']
    job_id = request.POST['job_id']
    sid = request.POST['sid']
    score = request.POST['sc']
    num = request.POST.get('num')
    st = request.POST.get('sta')
    # print(num)
    con = contestList.objects.filter(id=con_id)
    jobs = job.objects.filter(id=job_id)
    stu = Students.objects.filter(sid=sid)
    sta = station.objects.filter(id=st)
    str1 = json.loads(score)
    # 保存批量添加数组
    choice_score = []
    multiple_score = []
    judge_score = []
    # 竞赛评分
    score_type = con[0].type
    total_score = 0
    # 实训评分
    num_trues = 0

    # 你好啊233

    for c in str1[0]:
        iscore = False
        question = Choice.objects.filter(id=c['id'])
        if question[0].right_answer == c['answer']:
            iscore = True
        if score_type:
            if iscore:
                choice_score.append(
                    Choice_res(belong_contestList=con[0], belong_job=jobs[0], belong_question=question[0],
                               isscore=iscore, answer=c['answer'], sid=stu[0], score=question[0].score))
                total_score = total_score + question[0].score
            else:
                choice_score.append(
                    Choice_res(belong_contestList=con[0], belong_job=jobs[0], belong_question=question[0],
                               isscore=iscore, answer=c['answer'], sid=stu[0], score=0))
        else:
            choice_score.append(
                Choice_res(belong_contestList=con[0], belong_job=jobs[0], belong_question=question[0], isscore=iscore,
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
                    Multiple_res(belong_contestList=con[0], belong_job=jobs[0], belong_question=question[0],
                                 isscore=iscore,
                                 answer=str(list(filter(None, c['answer']))).replace("'", "\"").replace(r"\n", ""),
                                 sid=stu[0], score=question[0].score))
                total_score = total_score + question[0].score
            else:
                multiple_score.append(
                    Multiple_res(belong_contestList=con[0], belong_job=jobs[0], belong_question=question[0],
                                 isscore=iscore,
                                 answer=str(list(filter(None, c['answer']))).replace("'", "\"").replace(r"\n", ""),
                                 sid=stu[0], score=0))
        else:
            multiple_score.append(
                Multiple_res(belong_contestList=con[0], belong_job=jobs[0], belong_question=question[0], isscore=iscore,
                             answer=c['answer'], sid=stu[0]))
            if iscore:
                num_trues += 1
    for c in str1[2]:
        iscore = False
        question = Judge.objects.filter(id=c['id'])
        if question[0].right_answer == c['answer']:
            iscore = True
        if score_type:
            if iscore:
                judge_score.append(Judge_res(belong_contestList=con[0], belong_job=jobs[0], belong_question=question[0],
                                             isscore=iscore, answer=c['answer'], sid=stu[0], score=question[0].score))
                total_score = total_score + question[0].score
            else:
                judge_score.append(Judge_res(belong_contestList=con[0], belong_job=jobs[0], belong_question=question[0],
                                             isscore=iscore, answer=c['answer'], sid=stu[0], score=0))
        else:
            judge_score.append(
                Judge_res(belong_contestList=con[0], belong_job=jobs[0], belong_question=question[0], isscore=iscore,
                          answer=str(list(filter(None, c['answer']))).replace("'", "\"").replace(r"\n", ""),
                          sid=stu[0]))
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
                ch = Choice_res.objects.bulk_create(choice_score)
            if judge_score:
                ju = Judge_res.objects.bulk_create(judge_score)
            if multiple_score:
                mu = Multiple_res.objects.bulk_create(multiple_score)

            res = Results_job(belong_contestList=con[0], belong_job=jobs[0], sid=stu[0], score=total_score)
            res.save()
            # print(time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime()))
            return Response('ok')
    except:
        return Response('error')
    # return Response('ok')


# 表格
@api_view(['GET'])
def getTables(request):
    id = request.GET['id']
    con = contestList.objects.filter(id=id)
    jobs = job.objects.filter(contest=con[0])
    print(jobs)
    if len(jobs) > 0:
        datas = []
        data = {
            'conid': con[0].id,
            'contest': con[0].name,
            'record': datas
        }

        for j in jobs:
            # print(j)
            records = Record.objects.filter(belong_job=j)
            if len(records) > 0:
                rows = []
                columns = []
                data_item = {
                    'job': j.id,
                    'job_name': j.name,
                    'table': records[0].table,
                    'column_header': records[0].column_header,
                    'row_header': records[0].row_header,
                    'rows': rows,
                    'columns': columns,
                }
                rowes = Row.objects.filter(table=records[0])
                for r in rowes:
                    data_row = {
                        'id': r.id,
                        'type': r.type,
                        'name': r.row_name,
                    }
                    rows.append(data_row)
                col = Column.objects.filter(table=records[0])
                for co in col:
                    data_col = {
                        'id': co.id,
                        'name': co.column_name,
                    }
                    columns.append(data_col)

                datas.append(data_item)
        return Response(data)
    else:
        return Response('error')

    # 获取全部模块


@api_view(['GET'])
def getallmodels(request):
    id = request.GET['id']
    con = contestList.objects.filter(id=id, enable=True)
    if len(con) > 0:
        data = []
        if con[0].disorder:
            jobs = job.objects.filter(contest=con[0]).order_by('?')
        else:
            jobs = job.objects.filter(contest=con[0]).order_by('serial')
        if len(jobs) > 0:
            for j in jobs:
                data_item = {
                    'id': j.id,
                    'serial': j.serial,
                    'name': j.name,
                    'description': j.description,
                }
                data.append(data_item)
            return Response(data)
        else:
            return Response('None')
    else:
        return Response('error')


# 模块获取表格
@api_view(['GET'])
def model_table(request):
    # 根据模块ID获取该模块下对应的所有表格
    global tableList
    id = request.GET['id']
    jobs = job.objects.filter(id=id)
    if len(jobs) > 0:
        datas = []
        for j in jobs:
            # print(j)
            records = Record.objects.filter(belong_job=j)
            if len(records) > 0:
                tableList = []
                for record in records:
                    # 遍历一个模块中的多个表格
                    rows = []
                    columns = []
                    data_item = {
                        'job': j.id,
                        'job_name': j.name,
                        'table_id': record.id,
                        'table': record.table,
                        'column_header': record.column_header,
                        'row_header': record.row_header,
                        'rows': rows,
                        'columns': columns,
                    }
                    rowes = Row.objects.filter(table=record)
                    for r in rowes:
                        data_row = {
                            'id': r.id,
                            'type': r.type,
                            'name': r.row_name,
                        }
                        rows.append(data_row)
                    col = Column.objects.filter(table=record)
                    for co in col:
                        data_col = {
                            'id': co.id,
                            'name': co.column_name,
                        }
                        columns.append(data_col)

                    tableList.append(data_item)

            return Response(tableList)


# 提交表格内容
@api_view(['POST'])
def submitTable(request):
    con_id = request.POST['con_id']
    job_id = request.POST['job_id']
    sid = request.POST['sid']

    con = contestList.objects.filter(id=con_id).first()
    jobs = job.objects.filter(id=job_id).first()
    stu = Students.objects.filter(sid=sid).first()
    score_type = con.type

    numListT = request.POST['score_length']
    numList = json.loads(numListT[1:])

    scoreListT = request.POST['scoreList']
    scoreList = json.loads(scoreListT[1:])

    tableListT = request.POST['tableList']
    tableList = json.loads(tableListT[1:])

    tableIdListT = request.POST['tableIdList']
    tableIdList = json.loads(tableIdListT[1:])

    # num = request.POST.get('score_length')

    # 遍历该模块下的每个表格
    for i in range(len(tableList)):
        tab = tableIdList[i]
        score = scoreList[i]
        num = numList[i]

        table = Record.objects.filter(id=tab).first()

        # 单个表格的总分
        total_score = 0

        str1 = score

        # str1 = json.loads(score)

        table_score = []
        num_trues = 0
        try:
            for s in str1:
                # print(s)
                isscore = False
                row = Row.objects.filter(id=s['row_id']).first()
                column = Column.objects.filter(id=s['col_id']).first()
                # print(s['valueSelect'])
                if s['value']:
                    cri = Criteria.objects.filter(table=table, row=row, column=column).first()
                    # print(cri.type)
                    answer_type = cri.type
                    # print(answer_type)
                    if answer_type == "float":
                        right_answer = float(cri.answer)
                        min = right_answer - float(cri.error)
                        max = right_answer + float(cri.error)

                        if min <= float(s['value']) and float(s['value']) <= max:
                            isscore = True
                            if score_type:
                                total_score = total_score + cri.score
                                table_score.append(
                                    TableRecord(belong_contestList=con, belong_job=jobs, table=table, row=row,
                                                column=column,
                                                answer=s['value'], isscore=isscore, sid=stu, score=cri.score))
                            else:
                                num_trues += 1
                                table_score.append(
                                    TableRecord(belong_contestList=con, belong_job=jobs, table=table, row=row,
                                                column=column,
                                                answer=s['value'], isscore=isscore, sid=stu))
                        else:
                            table_score.append(
                                TableRecord(belong_contestList=con, belong_job=jobs, table=table, row=row,
                                            column=column,
                                            answer=s['value'], isscore=isscore, sid=stu))
                elif s['valueSelect']:
                    cri = Criteria.objects.filter(table=table, row=row, column=column).first()
                    answer_type = cri.type
                    right_answer = cri.judge_answer
                    print(s['valueSelect'])
                    if str(right_answer) == str(s['valueSelect']):
                        isscore = True
                        if score_type:
                            total_score = total_score + cri.score
                            table_score.append(
                                TableRecord(belong_contestList=con, belong_job=jobs, table=table, row=row,
                                            column=column,
                                            answer="判断题",
                                            judge_answer=s['valueSelect'], isscore=isscore, sid=stu, score=cri.score))
                        else:
                            num_trues += 1
                            table_score.append(
                                TableRecord(belong_contestList=con, belong_job=jobs, table=table, row=row,
                                            column=column,
                                            answer="判断题",
                                            judge_answer=s['valueSelect'], isscore=isscore, sid=stu))

                    else:
                        table_score.append(
                            TableRecord(belong_contestList=con, belong_job=jobs, table=table, row=row, column=column,
                                        answer="判断题",
                                        judge_answer=s['valueSelect'], isscore=isscore, sid=stu))

                else:
                    table_score.append(
                        TableRecord(belong_contestList=con, belong_job=jobs, table=table, row=row, column=column,
                                    answer="未做",
                                    isscore=isscore, sid=stu))
            if score_type:
                pass
            else:
                total_score = format(float(format(float(num_trues) / float(num), '.2f')) * 100, '.2f')
            with transaction.atomic():
                t = TableRecord.objects.bulk_create(table_score)
                # print(total_score)
                table_job_score = TableJobScore(belong_contestList=con, belong_job=jobs, belong_table=table, sid=stu, score=total_score)
                table_job_score.save()
        except Exception as e:
            print(e)
            return Response('error')
    # print(num)

    return Response('success')


@api_view(['GET'])
def checkTableScore(request):
    con_id = request.GET['con_id']
    job_id = request.GET['job_id']
    sid = request.GET['sid']
    tab = request.GET['tab_id']
    try:
        table = Record.objects.filter(id=tab).first()
        con = contestList.objects.filter(id=con_id).first()
        jobs = job.objects.filter(id=job_id).first()
        stu = Students.objects.filter(sid=sid).first()
        ta = TableRecord.objects.filter(belong_contestList=con, belong_job=jobs, sid=stu, table=table)
        if len(ta) > 0:
            return Response('same')
        else:
            return Response('None')
    except:
        return Response('error')


@api_view(['GET'])
def checkAllModels(request):
    con_id = request.GET.get('con_id')
    sid = request.GET.get('sid')
    con = contestList.objects.filter(id=con_id).first()
    stu = Students.objects.filter(sid=sid).first()
    jobs = job.objects.filter(contest=con)
    data = []
    try:
        for j in jobs:
            is_choice = False
            is_table = False
            res = Results_job.objects.filter(belong_contestList=con, belong_job=j, sid=stu)
            tab = TableJobScore.objects.filter(belong_contestList=con, belong_job=j, sid=stu)
            choice_list1 = Choice_job.objects.filter(belong_job_id=j.id)
            choice_list2 = Judge_job.objects.filter(belong_job_id=j.id)
            choice_list3 = Multiple_job.objects.filter(belong_job_id=j.id)

            if len(choice_list1) <= 0 & len(choice_list2) <= 0 & len(choice_list3) <= 0:
                is_choice = True

            if res:
                is_choice = True
            if tab:
                is_table = True
            data_item = {
                'id': j.id,
                'choice': is_choice,
                'table': is_table,
            }
            data.append(data_item)
        return Response(data)
    except:
        return Response('error')


@api_view(['POST'])
def addTableOnModule(request):
    # 获取json数据
    tables = request.POST['data']
    table_js = json.loads(tables)
    tableInfo = table_js['tableInfo']
    rowData = table_js['rowData']
    colData = table_js['colData']
    tableData = table_js['tableData']
    # 解析json
    try:
        with transaction.atomic():
            job_id = tableInfo['job_id'][1]
            # print(job_id)
            jobs = job.objects.filter(id=job_id).first()
            # print(jobs)
            rec = Record(belong_job=jobs, table=tableInfo['table_name'], column_header=tableInfo['col_header'],
                         row_header=tableInfo['row_header'])
            rec.save()
    except:
        return Response('error')
    row_source = []
    col_source = []
    cri_source = []
    # print(rec)
    try:
        for r in rowData:
            # print(r['type'])
            row_source.append(Row(table=rec, row_name=r['name'], type=r['type']))
        for c in colData:
            col_source.append(Column(table=rec, column_name=c['name']))

        with transaction.atomic():
            row_b = Row.objects.bulk_create(row_source)
            col_b = Column.objects.bulk_create(col_source)
        # for t in tableData:
        row = Row.objects.filter(table=rec)
        col = Column.objects.filter(table=rec)
        # print(row)
        for r_index, r in enumerate(rowData):
            for c_index, c in enumerate(colData):
                tab = "row-" + str(r_index + 1) + "-col-" + str(c_index + 1)
                # print(tab)
                # print(tableData[tab])
                print(tableData[tab]['answer'])
                if tableData[tab]['type'] == "float":

                    cri_source.append(
                        Criteria(table=rec, row=row[r_index], column=col[c_index], answer=tableData[tab]['answer'],
                                 score=tableData[tab]['score'], error=tableData[tab]['answerRange'],
                                 type=tableData[tab]['type']))
                elif tableData[tab]['type'] == "text":
                    cri_source.append(
                        Criteria(table=rec, row=row[r_index], column=col[c_index], answer=tableData[tab]['answer'],
                                 score=tableData[tab]['score'], error=tableData[tab]['answerRange'],
                                 type=tableData[tab]['type']))
                else:
                    cri_source.append(
                        Criteria(table=rec, row=row[r_index], column=col[c_index],
                                 judge_answer=tableData[tab]['answer'],
                                 score=tableData[tab]['score'], error=tableData[tab]['answerRange'],
                                 type=tableData[tab]['type']))

        with transaction.atomic():
            Criteria.objects.bulk_create(cri_source)
        return Response('success')
    except:
        return Response('error')


@api_view(['GET'])
def checkJobTable(request):
    job_id = request.GET['job_id']
    try:
        jobs = job.objects.filter(id=job_id).first()
        rec = Record.objects.filter(belong_job=jobs)
        if len(rec) > 0:
            return Response('same')
        else:
            return Response('None')
    except:
        return Response('error')


@api_view(['GET'])
def getStuWoring(request):
    con_id = request.GET['id']
    sid = request.GET['sid']
    contest = contestList.objects.filter(id=con_id).first()
    stu = Students.objects.filter(sid=sid).first()
    jobs = job.objects.filter(contest=contest)
    data = []
    for j in jobs:
        choice_data = []
        tables = []

        data_item = {
            'job_id': j.id,
            'job': j.name,
            'choice': choice_data,
            'tables': tables,
        }


        # 表名 contest_tablejobscore
        tab = TableJobScore.objects.filter(belong_contestList=contest, belong_job=j, sid=stu)

        # 遍历一个模块下的多个表格
        for tabsb in tab:

            # 根据belong_table_id获取表格详情
            tabInfo = Record.objects.filter(id=tabsb.belong_table_id)[0]

            # 该用户对此表格的作答详情
            tabs = TableRecord.objects.filter(table_id=tabsb.belong_table_id)

            row_Data = []
            column_Data = []
            table_Data = []
            table = {
              'tableName': tabInfo.table,
              'rows': row_Data,
              'columns': column_Data,
              'data': table_Data,
            }
            col = Column.objects.filter(table=tabInfo.id)
            for c in col:
                col_item = {
                    'tab_name': tabInfo.table,
                    'column_id': c.id,
                    'column_name': c.column_name,
                }
                column_Data.append(col_item)

            ro = Row.objects.filter(table=tabInfo.id)
            for r in ro:
                ro_item = {
                    'tab_name': tabInfo.table,
                    'row_id': r.id,
                    'row_name': r.row_name,
                    'type': r.type,
                }
                row_Data.append(ro_item)

            for t in tabs:
                cri = Criteria.objects.filter(table=t.table, row=t.row, column=t.column).first()
                table_item = {}

                if cri.type == "float":
                    table_item = {
                        'table': tabInfo.table,
                        'tab_id': tabInfo.id,
                        'row': t.row.row_name,
                        'row_id': t.row.id,
                        'column': t.column.column_name,
                        'column_id': t.column.id,
                        'answer': t.answer,
                        'error': cri.error,
                        'judge_answer': t.judge_answer,
                        'right_answer': cri.answer,
                        'isscore': t.isscore,
                        'score': t.score,
                    }
                elif cri.type == "select-1":
                    table_item = {
                        'table': tabInfo.table,
                        'tab_id': tabInfo.id,
                        'row': t.row.row_name,
                        'row_id': t.row.id,
                        'column': t.column.column_name,
                        'column_id': t.column.id,
                        'answer': t.answer,
                        'error': cri.error,
                        'judge_answer': t.judge_answer,
                        'right_answer': cri.judge_answer,
                        'isscore': t.isscore,
                        'score': t.score,
                    }
                elif cri.type == "text":
                    table_item = {
                        'table': tabInfo.table,
                        'tab_id': tabInfo.id,
                        'row': t.row.row_name,
                        'row_id': t.row.id,
                        'column': t.column.column_name,
                        'column_id': t.column.id,
                        'answer': t.answer,
                        'error': cri.error,
                        'judge_answer': t.judge_answer,
                        'right_answer': cri.answer,
                        'isscore': t.isscore,
                        'score': t.score,
                    }

                table_Data.append(table_item)

            tables.append(table)


        ch_res = Choice_res.objects.filter(belong_contestList=contest, belong_job=j, sid=stu)
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
                # print(choice_item)
                choice_data.append(choice_item)

        mu_res = Multiple_res.objects.filter(belong_contestList=contest, belong_job=j, sid=stu)
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
            # print()
            choice_data.append(multiple_item)
        ju_res = Judge_res.objects.filter(belong_contestList=contest, belong_job=j, sid=stu)
        for ju in ju_res:
            judge_item = {
                'question_id': ju.belong_question.id,
                'question': ju.belong_question.question,
                'isscore': ju.isscore,
                'score': ju.score,
                'answer': ju.answer,
                'type': 'judge',
            }
            choice_data.append(judge_item)
        # print(data_item)
        data.append(data_item)
    # print(data)
    return Response(data)

# 合分
@api_view(['POST'])
def mergeScore(request):
    sid = request.POST['sid']
    con_id = request.POST['con_id']
    tid = request.POST['tid']
    contest = contestList.objects.filter(id=con_id).first()
    stu = Students.objects.filter(sid=sid).first()
    teacher = Teachers.objects.filter(tid=tid).first()
    print(contest)
    print(stu)
    tab_score = 0
    choice_score = 0
    merge = Merge.objects.filter(belong_contestList=contest, sid=stu)
    if len(merge) > 0:
        return Response('error')
    else:
        # 表格成绩
        tab = TableJobScore.objects.filter(belong_contestList=contest, sid=stu)
        print(tab)
        if len(tab) > 0:
            for t in tab:
                tab_score = float(t.score) + float(tab_score)
        res = Results_job.objects.filter(belong_contestList=contest, sid=stu)
        print(res)
        if len(res) > 0:
            for r in res:
                choice_score = float(r.score) + float(choice_score)
        try:
            with transaction.atomic():
                m = Merge(belong_contestList=contest, sid=stu, score=choice_score, teacher=teacher, type="理论")
                m.save()
            with transaction.atomic():
                mt = Merge(belong_contestList=contest, sid=stu, score=tab_score, teacher=teacher, type="表格")
                mt.save()
        except:
            return Response('error')
        return Response('success')
