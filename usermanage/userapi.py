from rest_framework.decorators import api_view
from rest_framework.response import Response
from usermanage.models import Students, Teachers, Classes, Department
from django.contrib.auth.models import User, Permission, Group
from django.contrib.auth.hashers import check_password, make_password
from usermanage.serializers import StudentsSerializer, ClassesSerializer


@api_view(['POST'])
def stulogin(request):
    sid = request.POST['sid']
    password = request.POST['password']
    Stu = Students.objects.filter(sid=sid)
    if len(Stu) > 0:
        passwd = Stu[0].password
        if password == passwd:
            Std_data = StudentsSerializer(Stu[0])
            return Response(Std_data.data)
        else:
            return Response('pwderror')
    else:
        return Response('None')


@api_view(['GET', 'POST'])
def registerstu(request):
    if request.method == 'GET':
        classes = Classes.objects.all()
        cl = ClassesSerializer(classes, many=True)
        return Response(cl.data)
    else:
        sid = request.POST['sid']
        password = request.POST['password']
        name = request.POST['name']
        sex = request.POST['sex']
        classes = request.POST['class']
        try:
            stu_tmp = Students.objects.filter(sid=sid)
            if len(stu_tmp) > 0:
                return Response('same')
            else:
                newstu = Students(sid=sid, password=password, name=name, sex=sex,
                                  belong_class=Classes.objects.filter(id=classes)[0])
                newstu.save()
                return Response('register')
        except:
            return Response('error')


@api_view(['POST'])
def changepassword(request):
    sid = request.POST['sid']
    oldpassword = request.POST['oldpassword']
    password = request.POST['password']
    try:
        stu = Students.objects.get(sid=sid)
        if oldpassword == stu.password:
            stu.password = password
            stu.save()
            return Response('ok')
        else:
            return Response('olderror')
    except:
        return Response('error')


@api_view(['POST'])
def modifyclasses(request):
    sid = request.POST['sid']
    classes = request.POST['class']
    try:
        stu = Students.objects.get(sid=sid)
        cl = Classes.objects.filter(id=classes)
        stu.belong_class = cl[0]
        stu.save()
        return Response('ok')
    except:
        return Response('error')


@api_view(['GET'])
def getDepartment(request):
    de = Department.objects.all()
    data = []
    for d in de:
        data_item = {
            'id': d.id,
            'name': d.de_name
        }
        data.append(data_item)
    return Response(data)


@api_view(['POST'])
def register(request):
    tid = request.POST['tid']
    name = request.POST['name']
    sex = request.POST['sex']
    de = request.POST['depart']
    password = request.POST['password']
    user = User.objects.filter(username=tid)
    dep = Department.objects.filter(id=de)
    if user:
        return Response('same')
    else:
        try:
            newpwd = make_password(password, tid)
            newuser = User(username=tid, password=newpwd, is_staff=True)
            newuser.save()
        except:
            return Response('error')
        try:
            netTe = Teachers(tid=tid, name=name, sex=sex, belong_De=dep[0], belong_user=newuser)
            netTe.save()
            # print(2)
            # pers = Permission.objects.filter(
            #     codename__in=['delete_resources', 'change_choice_topic',
            #                   'curriculum.add_resources',
            #                   'view_multiple_choice_topic', 'add_examination',
            #                   'change_department', 'change_multiple_choice',
            #                   'view_judge_topic',
            #                   'view_results', 'change_examination',
            #                   'delete_multiple_choice_topic', 'view_choice_topic',
            #                   'view_judge', 'delete_examination', 'delete_results',
            #                   'delete_judge_topic', 'delete_multiple_choice',
            #                   'add_multiple_choice_topic', 'change_students',
            #                   'add_multiple_choice', 'add_examinations',
            #                   'add_questiontype',
            #                   'view_multiple_choice', 'delete_choice',
            #                   'change_multiple_choice_topic', 'add_classes',
            #                   'curriculum.delete_course',
            #                   'change_choice', 'view_students', 'delete_choice_topic',
            #                   'view_department', 'delete_judge', 'curriculum.add_course',
            #                   'curriculum.view_course', 'add_judge', 'delete_questiontype',
            #                   'data.view_choice', 'data.change_choice', 'view_choice',
            #                   'delete_examinations', 'data.delete_choice', 'add_judge_topic',
            #                   'add_department', 'delete_department', 'add_choice',
            #                   'change_judge', 'delete_students', 'add_choice_topic',
            #                   'change_results', 'delete_classes', 'curriculum.change_course',
            #                   'curriculum.change_resources', 'change_judge_topic',
            #                   'add_results',
            #                   'view_examination', 'view_questiontype',
            #                   'view_examinations',
            #                   'add_students', 'change_examinations', 'curriculum.view_resources',
            #                   'data.add_choice', 'view_classes', 'change_classes',
            #                   'change_questiontype'])
            # print(pers)
            # # pers = user[0].get_all_permissions()
            # # datas = []
            # # for p in pers:
            # #     datas.append(p)
            # # print(datas)
            # # print(pers)
            # # print()
            # for pe in pers:
            #     newuser.user_permissions.add(pe)
            # newuser.save()
            tegroup = Group.objects.filter(name="teacher").first()
            newuser.is_staff = True
            newuser.groups.add(tegroup)
            return Response('success')
        except:
            newuser.delete()
            return Response('error')


@api_view(['POST'])
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    print(username, password)
    user = User.objects.filter(username=username)
    if len(user) > 0:
        # print(user)
        user_pwd = user[0].password
        auth_pwd = check_password(password, user_pwd)
        # print(auth_pwd)
        if auth_pwd:
            userinfo = Teachers.objects.filter(belong_user=user[0], enable=True)
            if userinfo:
                data = {
                    'name': userinfo[0].name,
                    'tid': userinfo[0].tid,
                    'department': userinfo[0].belong_De.de_name,
                    'sex': userinfo[0].sex,
                }
                return Response(data)
            else:
                return Response('error')
        else:
            return Response('pwderr')

    else:
        return Response('None')


@api_view(['POST'])
def login(request):
    username = request.POST['username']
    password = request.POST['password']

    user = User.objects.filter(username=username)
    if len(user) > 0:
        # print(user)
        user_pwd = user[0].password
        auth_pwd = check_password(password, user_pwd)
        # print(auth_pwd)
        if auth_pwd:
            userinfo = Teachers.objects.filter(belong_user=user[0], enable=True)
            if userinfo:
                data = {
                    'name': userinfo[0].name,
                    'tid': userinfo[0].tid,
                    'department': userinfo[0].belong_De.de_name,
                    'sex': userinfo[0].sex,
                }
                return Response(data)
            else:
                return Response('error')
        else:
            return Response('pwderr')

    else:
        return Response('None')
