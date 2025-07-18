from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from curriculum.serializers import CourseSerializers, ResourcesSerializers
from rest_framework.decorators import api_view
from curriculum.models import Course, Resources, Resources_views

# Create your views here.
from usermanage.models import Students


class CourseListViewSet(ModelViewSet):
    queryset = Course.objects.filter(enable=True)
    serializer_class = CourseSerializers


@api_view(['GET'])
def getResources(request):
    id = request.GET['id']
    cou = Course.objects.filter(id=id)
    if cou:
        res = Resources.objects.filter(belong_course=cou[0].id).order_by('serial')
        if res:
            res_data = ResourcesSerializers(res, many=True)
            return Response(res_data.data)
        else:
            return Response('None')
    else:
        return Response('error')

@api_view(['POST'])
def subViews(request):
    sid = int(request.POST['sid'])
    rid = int(request.POST['rid'])
    try:
        stu = Students.objects.filter(sid=sid).first()
        res = Resources.objects.filter(id=rid).first()
        res_view = Resources_views(belong_resources=res, sid=stu, belong_class_id=stu.belong_class_id)
        res_view.save()
        num = int(res.views) + 1
        res.views = num
        res.save()
    except:
        return Response("error")
    return Response("success")