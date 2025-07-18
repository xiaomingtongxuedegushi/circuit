from django.db import models
from django.utils.html import format_html

from usermanage.models import Students, Teachers
from question.models import Choice, Multiple_Choice, Judge


# Create your models here.


class elecontest(models.Model):
    TYPE_CHOICES = (
        (0, '实训'),
        (1, '竞赛')
    )

    name = models.CharField("竞赛名称", max_length=50)
    enable = models.BooleanField("启用", default=False)
    type = models.IntegerField("类型", choices=TYPE_CHOICES, default=0)
    start_date = models.DateTimeField("开始时间", null=True, blank=True)
    end_date = models.DateTimeField("结束时间", null=True, blank=True)
    fault = models.TextField("故障设置", max_length=5000, null=True, blank=True)
    file = models.FileField("工单", upload_to='electron/', null=True, blank=True)
    remarks = models.CharField("备注", max_length=500, null=True, blank=True)
    class Meta:
        verbose_name = '电子竞赛'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class EleRecord(models.Model):
    belong_ele = models.ForeignKey(elecontest, on_delete=models.CASCADE, verbose_name="电子竞赛")
    sid = models.ForeignKey(Students, on_delete=models.CASCADE, verbose_name="学生名字", null=True,
                            blank=True)
    file = models.FileField("工单", upload_to='electron/', null=True, blank=True)

    def file_open(self):
        return format_html(
            '<a href="javascript:;" onclick="window.bound.openfileselect(\'{}\')">查看文件</a>',
            self.file
        )

    file_open.short_description = '查看工单文件2'

    class Meta:
        verbose_name = '工单记录'
        verbose_name_plural = verbose_name

    def __init(self):
        return self.id


class Choice_ele(models.Model):
    belong_ele = models.ForeignKey(elecontest, on_delete=models.CASCADE, verbose_name="电子竞赛")
    belong_question = models.ForeignKey(Choice, on_delete=models.CASCADE, verbose_name="题目")

    class Meta:
        ordering = ['id']
        verbose_name = '题目'
        verbose_name_plural = '选择题目'

    def __init(self):
        return self.id


class Multiple_ele(models.Model):
    belong_ele = models.ForeignKey(elecontest, on_delete=models.CASCADE, verbose_name="电子竞赛")
    belong_question = models.ForeignKey(Multiple_Choice, on_delete=models.CASCADE, verbose_name="题目")

    class Meta:
        ordering = ['id']
        verbose_name = '题目'
        verbose_name_plural = '多选题目'

    def __init(self):
        return self.id


class Judge_ele(models.Model):
    belong_ele = models.ForeignKey(elecontest, on_delete=models.CASCADE, verbose_name="电子竞赛")
    belong_question = models.ForeignKey(Judge, on_delete=models.CASCADE, verbose_name="题目")

    class Meta:
        ordering = ['id']
        verbose_name = '题目'
        verbose_name_plural = '判断题目'

    def __init(self):
        return self.id


class Choice_res_ele(models.Model):
    belong_ele = models.ForeignKey(elecontest, on_delete=models.CASCADE, verbose_name="电子竞赛", null=True, blank=True)
    belong_question = models.ForeignKey(Choice, on_delete=models.CASCADE, verbose_name="题目")
    isscore = models.BooleanField("得分", default=False)
    score = models.DecimalField(verbose_name='分值', decimal_places=2, max_digits=5, null=True, blank=True)
    answer = models.CharField("答题", max_length=10)
    sid = models.ForeignKey(Students, on_delete=models.CASCADE, verbose_name="学生名字")

    class Meta:
        ordering = ['id']
        verbose_name = '选择题记录'
        verbose_name_plural = '选择题记录'

    def __init(self):
        return self.id


class Multiple_res_ele(models.Model):
    belong_ele = models.ForeignKey(elecontest, on_delete=models.CASCADE, verbose_name="电子竞赛", null=True, blank=True)
    belong_question = models.ForeignKey(Multiple_Choice, on_delete=models.CASCADE, verbose_name="题目")
    isscore = models.BooleanField("得分", default=False)
    score = models.DecimalField(verbose_name='分值', decimal_places=2, max_digits=5, null=True, blank=True)
    answer = models.CharField("答题", max_length=10)
    sid = models.ForeignKey(Students, on_delete=models.CASCADE, verbose_name="学生名字")

    class Meta:
        ordering = ['id']
        verbose_name = '多选题记录'
        verbose_name_plural = verbose_name

    def __init(self):
        return self.id


class Judge_res_ele(models.Model):
    belong_ele = models.ForeignKey(elecontest, on_delete=models.CASCADE, verbose_name="电子竞赛", null=True, blank=True)
    belong_question = models.ForeignKey(Judge, on_delete=models.CASCADE, verbose_name="题目")
    isscore = models.BooleanField("得分", default=False)
    score = models.DecimalField(verbose_name='分值', decimal_places=2, max_digits=5, null=True, blank=True)
    answer = models.CharField("答题", max_length=10)
    sid = models.ForeignKey(Students, on_delete=models.CASCADE, verbose_name="学生名字")
    class Meta:
        ordering = ['id']
        verbose_name = '判断题记录'
        verbose_name_plural = verbose_name

    def __init(self):
        return self.id


class station_ele(models.Model):
    name = models.CharField("工位号", max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '工位'
        verbose_name_plural = verbose_name


class Results_ele(models.Model):
    TYPE_CHOICES = (
        ('评分', '评分'),
        ('理论', '理论')
    )
    belong_ele = models.ForeignKey(elecontest, on_delete=models.CASCADE, verbose_name="电子竞赛")
    belong_sta = models.ForeignKey(station_ele, on_delete=models.CASCADE,verbose_name="工位号",null=True, blank=True)
    sid = models.ForeignKey(Students, on_delete=models.CASCADE, verbose_name="学生名字")
    score = models.DecimalField(verbose_name='分数', decimal_places=1, max_digits=5)
    submit = models.DateTimeField("提交时间", auto_now_add=True)

    class Meta:
        ordering = ['id']
        verbose_name = '成绩'
        verbose_name_plural = '学生成绩'

    def __init(self):
        return self.id
