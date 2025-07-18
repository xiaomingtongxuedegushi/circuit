from datetime import datetime, timezone

from django.db import models
from usermanage.models import Classes, Teachers, Students
from question.models import Choice, Multiple_Choice, Judge


# Create your models here.
#   考试题目
class Examinations(models.Model):
    name = models.CharField("考试名称", max_length=50)
    enable = models.BooleanField(verbose_name='启用', default=False)
    show = models.BooleanField("查看试卷", default=True)
    disorder = models.BooleanField("题目乱序", default=True)
    start_date = models.DateTimeField(verbose_name="开始时间", default=datetime.now())
    end_date = models.DateTimeField("结束时间", default=datetime.now())
    duration = models.IntegerField("时长", default=120)
    group = models.ForeignKey(Classes, on_delete=models.CASCADE, related_name="gr_cl", verbose_name="考试班级",
                              default=Classes.objects.all()[0].id)
    belong_te = models.ForeignKey(Teachers, on_delete=models.CASCADE, related_name="be_te", verbose_name="教师",
                                )
    remarks = models.CharField("备注", max_length=200, null=True, blank=True)

    class Meta:
        ordering = ['id']
        verbose_name = '考试名称'
        verbose_name_plural = '考试管理'

    def __str__(self):
        return self.name


class Choice_Topic(models.Model):
    belong_name = models.ForeignKey(Examinations, on_delete=models.CASCADE, related_name="bl_name", verbose_name="考试名称")
    belong_question = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name="bl_name", verbose_name="题目")

    class Meta:
        ordering = ['id']
        verbose_name = '题目'
        verbose_name_plural = '选择题目'

    def __init(self):
        return self.id


class Multiple_Choice_Topic(models.Model):
    belong_name = models.ForeignKey(Examinations, on_delete=models.CASCADE, related_name=None, verbose_name="考试名称")
    belong_question = models.ForeignKey(Multiple_Choice, on_delete=models.CASCADE, related_name=None, verbose_name="题目")

    class Meta:
        ordering = ['id']
        verbose_name = '题目'
        verbose_name_plural = '多选题目'

    def __init(self):
        return self.id


class Judge_Topic(models.Model):
    belong_name = models.ForeignKey(Examinations, on_delete=models.CASCADE, related_name=None, verbose_name="考试名称")
    belong_question = models.ForeignKey(Judge, on_delete=models.CASCADE, related_name=None, verbose_name="题目")

    class Meta:
        ordering = ['id']
        verbose_name = '题目'
        verbose_name_plural = '判断题目'

    def __init(self):
        return self.id


class Results(models.Model):
    name = models.ForeignKey(Examinations, on_delete=models.CASCADE, related_name=None, verbose_name="考试名称")
    sid = models.ForeignKey(Students, on_delete=models.CASCADE, related_name=None, verbose_name="学生名字")
    score = models.DecimalField(verbose_name='分数', decimal_places=1, max_digits=5)
    submit = models.DateTimeField("提交时间", auto_now_add=True)

    class Meta:
        ordering = ['id']
        verbose_name = '成绩'
        verbose_name_plural = '学生成绩'

    def __init(self):
        return self.id
