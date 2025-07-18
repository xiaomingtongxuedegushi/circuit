import urllib
from urllib.request import Request

from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render

from usermanage import userapi

from rest_framework.decorators import api_view
from rest_framework.response import Response
from data.models import Fault, Classification, Userinfo, serial
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password, make_password

from usermanage.models import Teachers


@api_view(['GET'])
def toPage(request):
    url = request.GET['url']

    decode_url = urllib.parse.unquote(url)

    username = request.GET['username']
    password = request.GET['password']

    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return HttpResponseRedirect(decode_url)
    else:
        return Response('用户名或密码错误')



@api_view(['GET'])
def getport(request):
    if request.method == 'GET':
        s = serial.objects.all()
        data = {
            'fault': s[0].port,
            'test': s[1].port,
        }
        return Response(data)


@api_view(['POST'])
def toLogin(request):
    # print(request.POST)
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
            userinfo = Userinfo.objects.filter(belong_user=user[0])
            if userinfo:
                return Response('ok')
            else:
                return Response('error')
        else:
            return Response('pwderr')

    else:
        return Response('None')


@api_view(['POST'])
def toRegister(request):
    username = request.POST['username']
    password = request.POST['password']
    # password2 = request.POST['password2']
    # print(username, password,password2)
    user = User.objects.filter(username=username)
    if user:
        return Response('same')
    else:
        newpwd = make_password(password, username)
        newuser = User(username=username, password=newpwd)
        newuser.save()
    return Response('ok')


@api_view(['GET'])
def get_fault_list(request):
    class_name = request.GET['name']
    # print(class_name)
    classification = Classification.objects.filter(class_name=class_name)
    # print(classification)
    fault = Fault.objects.filter(belong_class=classification[0])
    data = []
    for f in fault:
        data_item = {
            'id': f.id,
            'name': f.name,
            'card': f.card,
            'address': f.address,
            'status': f.status,

        }
        data.append(data_item)
    # print(data)
    # fault_data = Fault_data(fault,many=True)
    return Response(data)


@api_view(['POST'])
def get_address(request):
    id = request.POST['id']
    fault = Fault.objects.filter(id=id)
    if fault:
        data = {
            'card': fault[0].card,
            'address': fault[0].address,
        }
        return Response(data)
    return Response('error')


@api_view(['POST'])
def alter_status(request):
    id = request.POST['id']
    status = request.POST['status']
    # print(request)
    fault = Fault.objects.get(id=id)
    fault.status = status

    if fault.save():
        return Response('error')
    else:
        return Response('ok')


@api_view(['POST'])
def set_all_status(request):
    belong_class = request.POST['class']
    classification = Classification.objects.filter(class_name=belong_class)
    fault = Fault.objects.filter(belong_class=classification[0])
    print(fault)
    for f in fault:
        if f.status != 0:
            f.status = 0
            f.save()

    return Response('ok')
