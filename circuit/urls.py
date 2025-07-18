
"""circuit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include, re_path
from django.contrib import admin
from django.urls import path

import curriculum
import electron.views
from curriculum import views
import examination.views
import contest.views
from data import api, mph
from question import questionapi
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from contest.tableScoreapi import TableRecordListViewSet
from question.views import ChoiceListViewSet, MultipleViewsView, JudgeViewsView
from examination.views import ExadminationsListViewSet
from curriculum.views import CourseListViewSet
from rest_framework.routers import DefaultRouter, SimpleRouter
from usermanage import userapi

router = SimpleRouter(
)
router.register(r'choices', ChoiceListViewSet)
router.register(r'examine', ExadminationsListViewSet)
router.register(r'course', CourseListViewSet)
router.register(r'multiple', MultipleViewsView)
router.register(r'judge', JudgeViewsView)
router.register(r'table', TableRecordListViewSet)
urlpatterns = [
                  path('resources_subView/', curriculum.views.subViews),

                  path('resources_monitor/', mph.resources_monitor),
                  path('set_point_data/', mph.set_point_data),
                  path('set_point_image/', mph.set_point_image),

                  path('upload_point_data/', mph.upload_point_data),
                  path('upload_point_image/', mph.upload_point_image),

                  path('toPage/', api.toPage),

                  path('admin/', admin.site.urls),
                  path('login/', userapi.login),
                #   path('register/', api.toRegister),
                  path('getport/', api.getport),
                  path('get_fault_list/', api.get_fault_list),
                  path('alter_status/', api.alter_status),
                  path('get_address/', api.get_address),
                  path('set_all_status/', api.set_all_status),
                  path('get_choices/', questionapi.get_choices),
                  path('get_judges/', questionapi.get_judges),
                  path('get_multiple_choice/', questionapi.get_multiple_choice),
                  path('stulogin/', userapi.stulogin),
                  path('registerstu/', userapi.registerstu),
                  path('changepassword/', userapi.changepassword),
                  path('modifyclasses/', userapi.modifyclasses),
                  path('examin/', examination.views.getexamin),
                  path('getchoice_topic/', examination.views.getchoice_topic),
                  path('getmultiple_topic/', examination.views.getMultiple_Choice_Topic),
                  path('getjudge_topic/', examination.views.getJudge_Topic),
                  # 考试快速添加
                  path('addchoice/', examination.views.addChoice),
                  path('addmutiple/', examination.views.addMutiple),
                  path('addjudge/', examination.views.addJudge),
                  path('delchoice/', examination.views.delChoice),
                  path('delmutiple/', examination.views.delMutiple),
                  path('deljudge/', examination.views.delJudge),
                  path('getexinfo/', examination.views.getexInfo),
                  path('getResources/', curriculum.views.getResources),
                  path('subgrades/', examination.views.subGrades),
                  # 快速选择获取类型
                  path('getGrades/', examination.views.getGrades),
                  path('getquestion_type/', questionapi.get_QuestionType),
                  path('getclass/', questionapi.get_classification),
                  path('getexam/', questionapi.getExamList),

                  path('getstep/', contest.views.get_step),
                  path('getjob/', contest.views.get_job),
                  path('subjobscore/', contest.views.subJobscore),
                  path('getjobtotal/', contest.views.getjobTotal),
                  path('posttotal/', contest.views.postTotal),
                  path('getcontest/', contest.views.getContest),
                  path('getcriteria/', contest.views.getCriteria),
                  path('testlogin/', contest.views.testlogin),
                  # 考试
                  path('get_job_model/', contest.views.get_job_model),  # 获取模块列表
                  path('get_exam_len/', contest.views.get_exam_len),  # 获取模块下题目数量
                  path('addchoice_job/', contest.views.addChoice_job),
                  path('addmutiple_job/', contest.views.addMutiple_job),
                  path('addjudge_job/', contest.views.addJudge_job),
                  path('delchoice_job/', contest.views.delChoice_job),
                  path('delmutiple_job/', contest.views.delMutiple_job),
                  path('deljudge_job/', contest.views.delJudge_job),
                  path('getjobchoices/', contest.views.getjobchoices),  # 获取所有题目
                  path('post_job_choice/', contest.views.post_job_choice),  # 提交理论成绩
                  path('getJobisSCore/', contest.views.get_job_isscore),  # 判断模块是否存在理论成绩

                  # 表格
                  path('gettables/', contest.views.getTables),  # 获取表格
                  path('getallmodels/', contest.views.getallmodels),  # 获取模块
                  path('model_table/', contest.views.model_table),  # 获取模块下的表格
                  path('submitTable/', contest.views.submitTable),  # 提交表格
                  path('checkTableScore/', contest.views.checkTableScore),  # 判断是否存在表格成绩

                  path('checkAllModels/', contest.views.checkAllModels),  # 判断考试下，是否存在成绩

                  path('addTableOnModule/', contest.views.addTableOnModule),  # 添加表格
                  path('checkJobTable/', contest.views.checkJobTable),  # 检查模块下是否存在表格
                  path('getStuWoring/', contest.views.getStuWoring),  # 获取学生错题
                  path('mergeScore/', contest.views.mergeScore),  # 合并成绩

                  # 电子竞赛
                  path('getEle/', electron.views.getEle),
                  path('getEleList/', electron.views.getEleList),  # 获取竞赛列表——快速添加
                  path('getEleinfo/', electron.views.getEleinfo),  # 获取竞赛理论信息
                  path('addchoice_ele/', electron.views.addChoice_ele),  # 快速添加Api
                  path('addmutiple_ele/', electron.views.addMutiple_ele),
                  path('addjudge_ele/', electron.views.addJudge_ele),
                  path('delchoice_ele/', electron.views.delChoice_ele),
                  path('delmutiple_ele/', electron.views.delMutiple_ele),
                  path('deljudge_ele/', electron.views.delJudge_ele),
                  path('getElechoices/', electron.views.getElechoices),
                  path('post_ele_choice/', electron.views.post_ele_choice),  # 提交电子竞赛理论成绩
                  path('getScore/',electron.views.getScore),
                  path('subFiles/',electron.views.subFiles),
                  path('checkEleScore/',electron.views.checkEleScore),# 检查成绩
                  path('eleLogin/',electron.views.eleLogin),# 登录电子竞赛
                  path('register/',userapi.register),

                  #客户端api
                  path('getDepartment/',userapi.getDepartment),#获取院系列表
                  re_path('^', include(router.urls)),
                  re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
