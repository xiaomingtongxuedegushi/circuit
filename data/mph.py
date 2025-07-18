from multiprocessing import context

import os

from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from circuit.settings import MEDIA_ROOT
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def resources_monitor(request):
    return render(request, "resources_monitor.html")

@api_view(['GET'])
def set_point_image(request):
    return render(request, "set_point_image.html")

@api_view(['GET'])
def set_point_data(request):
    file_url = os.path.join(MEDIA_ROOT, "point_setting.json").replace('\\', '/')

    data = ''
    try:
        with open(file_url, 'r', encoding='utf-8') as f:
            data = f.read()
    except:
        print("读取文件错误")

    return render(request, "set_point_data.html", {
        'data': data
    })


@csrf_exempt
@api_view(['POST'])
def upload_point_data(request):

    point_data = request.POST['point_data']

    print(point_data)
    if point_data:
        try:
            file_url = os.path.join(MEDIA_ROOT, "point_setting.json").replace('\\', '/')
            print(file_url)
            with open(file_url, 'w', encoding='utf-8') as f:
                f.write(str(point_data))
            return HttpResponseRedirect("/set_point_data/")
        except Exception as e:
            print(e)
            return Response('error')
    else:
        return Response('None')

@csrf_exempt
@api_view(['POST'])
def upload_point_image(request):
    file = request.FILES.get('file')
    print(file)
    if file:
        try:
            file_url = os.path.join(MEDIA_ROOT, "point_image.png").replace('\\', '/')
            print(file_url)
            with open(file_url, 'wb+') as f:
                for i in file:
                    f.write(i)
            return HttpResponseRedirect("/set_point_image/")
        except:
            return Response('error')
    else:
        return Response('None')