from django.db import models
from usermanage.models import Students, Teachers
from django.utils.html import format_html
from question.models import Choice, Multiple_Choice, Judge


# Create your models here.
class contestList(models.Model):
    TYPE_CHOICES = (
        (0, '实训'),
        (1, '竞赛')
    )
    name = models.CharField("竞赛名称", max_length=50)
    enable = models.BooleanField("启用", default=False)
    disorder = models.BooleanField("模块乱序", default=False)
    images = models.ImageField("展示图", upload_to='contestList/', null=True, blank=True)
    pdfs = models.FileField("评分标准PDF文档", upload_to='contestListPdf/', null=True, blank=True)
    type = models.IntegerField("类型", choices=TYPE_CHOICES, default=0)
    start_date = models.DateTimeField("开始时间", null=True, blank=True)
    end_date = models.DateTimeField("结束时间", null=True, blank=True)

    class Meta:
        verbose_name = '竞赛'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class station(models.Model):
    name = models.CharField("工位号", max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '工位'
        verbose_name_plural = verbose_name


class Modula(models.Model):
    name = models.CharField("模块名称", max_length=50)
    belong_contest = models.ForeignKey(contestList, on_delete=models.CASCADE, verbose_name="竞赛", blank=True, null=True)

    class Meta:
        verbose_name = '模块'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class project(models.Model):
    name = models.CharField("项目", max_length=50)
    belong_modula = models.ForeignKey(Modula, on_delete=models.CASCADE, verbose_name="模块", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '项目'
        verbose_name_plural = verbose_name


class step(models.Model):
    name = models.CharField("步骤", max_length=50)
    tools = models.CharField("工具", max_length=100, null=True, blank=True)
    images = models.ImageField("展示图", upload_to='contest/', null=True, blank=True)
    programme = models.CharField("方案", max_length=100, blank=True, null=True)
    attention = models.CharField("注意事项", max_length=100, blank=True, null=True)
    belong_project = models.ForeignKey(project, on_delete=models.CASCADE, verbose_name="项目", blank=True, null=True)

    def __str__(self):
        return self.name

    def image_data(self):
        return format_html(
            '<img src="{}" width="100px"/>',
            self.images.url,
        )

    image_data.short_description = u'当前图片'

    class Meta:
        verbose_name = '步骤'
        verbose_name_plural = verbose_name


class job(models.Model):
    name = models.CharField("作业项目", max_length=50)
    serial = models.IntegerField("序号", blank=True, null=True)
    description = models.CharField("简介", max_length=50, default='无')
    contest = models.ForeignKey(contestList, null=True, blank=True, on_delete=models.CASCADE, verbose_name="竞赛")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '作业项目'
        verbose_name_plural = verbose_name


class job_item(models.Model):
    name = models.CharField("作业小项", max_length=50)
    score = models.DecimalField(verbose_name='配分', decimal_places=2, max_digits=5, null=True, blank=True)
    belong_job = models.ForeignKey(job, on_delete=models.CASCADE, verbose_name="作业项目")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '作业小项'
        verbose_name_plural = verbose_name


class jobScore(models.Model):
    belong_contestList = models.ForeignKey(contestList, on_delete=models.CASCADE, verbose_name="竞赛", null=True,
                                           blank=True)
    studen = models.ForeignKey(Students, on_delete=models.CASCADE, verbose_name="学生")
    belong_st = models.ForeignKey(station, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="工位号")
    belong_job = models.ForeignKey(job, on_delete=models.CASCADE, verbose_name="作业项目")
    belong_job_item = models.ForeignKey(job_item, on_delete=models.CASCADE, verbose_name="作业小项目")
    score = models.DecimalField(verbose_name='配分', decimal_places=1, max_digits=5)
    teacher = models.ForeignKey(Teachers, on_delete=models.CASCADE, verbose_name="裁判")

    class Meta:
        verbose_name = '配分'
        verbose_name_plural = verbose_name


class jobTotal(models.Model):
    belong_contestList = models.ForeignKey(contestList, on_delete=models.CASCADE, verbose_name="竞赛")
    studen = models.ForeignKey(Students, on_delete=models.CASCADE, verbose_name="学生")
    belong_st = models.ForeignKey(station, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="工位号")
    score = models.DecimalField(verbose_name='总分', decimal_places=1, max_digits=5, default='0')
    teacher = models.ForeignKey(Teachers, on_delete=models.CASCADE, verbose_name="裁判")
    images = models.ImageField("裁判签名", upload_to='jobTotal/', null=True, blank=True)
    submit = models.DateTimeField("开始时间", auto_now_add=True)
    alter_time = models.DateTimeField("修改时间", auto_now=True)

    @property
    def face_image_url(self):  # 这一段很关键要加上
        if self.images and hasattr(self.images, 'url'):
            return self.images.url

    class Meta:
        verbose_name = '总分'
        verbose_name_plural = verbose_name


class Record(models.Model):
    belong_job = models.ForeignKey(job, on_delete=models.CASCADE, verbose_name="作业项目", null=True, blank=True)
    table = models.CharField("表格名", max_length=50)
    column_header = models.CharField("列表头", max_length=10)
    row_header = models.CharField("行表头", max_length=10)

    def __str__(self):
        return self.table

    class Meta:
        verbose_name = '记录表'
        verbose_name_plural = verbose_name


class Row(models.Model):
    TYPE_CHOICES = (
        ('float', '测量题'),
        ('text', '描述题'),
        ('select-1', '判断题')
    )
    table = models.ForeignKey(Record, on_delete=models.CASCADE, verbose_name="表格")
    row_name = models.CharField("行名称", max_length=50)
    type = models.CharField(verbose_name="类型", max_length=10, choices=TYPE_CHOICES, default='数值')

    def __str__(self):
        return self.row_name

    class Meta:
        verbose_name = '行'
        verbose_name_plural = verbose_name


class Column(models.Model):
    table = models.ForeignKey(Record, on_delete=models.CASCADE, verbose_name="表格")
    column_name = models.CharField("列名称", max_length=50)

    def __str__(self):
        return self.column_name

    class Meta:
        verbose_name = '列'
        verbose_name_plural = verbose_name


class Criteria(models.Model):
    TYPE_CHOICES = (
        ('float', '数值题'),
        ('text', '描述题'),
        ('select-1', '判断题')
    )
    Judge_CHOICES = (
        (1, '正常'),
        (2, '维修'),
        (3, '更换'),
        (4, '调整')
    )
    table = models.ForeignKey(Record, on_delete=models.CASCADE, verbose_name="表格", blank=True, null=True)
    row = models.ForeignKey(Row, on_delete=models.CASCADE, verbose_name="行")
    column = models.ForeignKey(Column, on_delete=models.CASCADE, verbose_name="列")
    answer = models.CharField(verbose_name='正确值', max_length=50, null=True, blank=True)
    judge_answer = models.IntegerField(verbose_name="判断正确值", choices=Judge_CHOICES, blank=True, null=True)
    error = models.DecimalField(verbose_name='误差', decimal_places=1, max_digits=5, default='0', null=True, blank=True)
    score = models.DecimalField(verbose_name='分值', decimal_places=2, max_digits=5, default='2', null=True, blank=True)
    type = models.CharField(verbose_name='类型', max_length=10, choices=TYPE_CHOICES)

    def __init(self):
        return self.id

    class Meta:
        verbose_name = '作答标准'
        verbose_name_plural = verbose_name


class TableRecord(models.Model):
    Judge_CHOICES = (
        (1, '正常'),
        (2, '维修'),
        (3, '更换'),
        (4, '调整')
    )
    belong_contestList = models.ForeignKey(contestList, on_delete=models.CASCADE, verbose_name="竞赛")
    belong_job = models.ForeignKey(job, on_delete=models.CASCADE, verbose_name="作业项目")
    sid = models.ForeignKey(Students, on_delete=models.CASCADE, related_name=None, verbose_name="学生名字", null=True,
                            blank=True)
    table = models.ForeignKey(Record, on_delete=models.CASCADE, verbose_name="表格")
    row = models.ForeignKey(Row, on_delete=models.CASCADE, verbose_name="行")
    column = models.ForeignKey(Column, on_delete=models.CASCADE, verbose_name="列")
    answer = models.CharField(verbose_name='答题', max_length=50)
    judge_answer = models.IntegerField(verbose_name="判断答题值", choices=Judge_CHOICES, blank=True, null=True)
    isscore = models.BooleanField("得分", default=False)
    score = models.DecimalField(verbose_name='分值', decimal_places=2, max_digits=5, null=True, blank=True)

    class Meta:
        ordering = ['id']
        verbose_name = '答题记录'
        verbose_name_plural = '答题记录'

    def __init(self):
        return self.id


class TableJobScore(models.Model):
    belong_contestList = models.ForeignKey(contestList, on_delete=models.CASCADE, verbose_name="竞赛")
    belong_job = models.ForeignKey(job, on_delete=models.CASCADE, verbose_name="作业项目")
    belong_table = models.ForeignKey(Record, on_delete=models.CASCADE, verbose_name="表格")
    sid = models.ForeignKey(Students, on_delete=models.CASCADE, related_name=None, verbose_name="学生名字", null=True,
                            blank=True)
    score = models.DecimalField(verbose_name='分数', decimal_places=1, max_digits=5)
    submit = models.DateTimeField("提交时间", auto_now_add=True)

    class Meta:
        ordering = ['id']
        verbose_name = '表格成绩'
        verbose_name_plural = '表格成绩'

    def __init(self):
        return self.id


class Choice_job(models.Model):
    belong_job = models.ForeignKey(job, on_delete=models.CASCADE, verbose_name="作业项目")
    belong_question = models.ForeignKey(Choice, on_delete=models.CASCADE, verbose_name="题目")

    class Meta:
        ordering = ['id']
        verbose_name = '题目'
        verbose_name_plural = '选择题目'

    def __init(self):
        return self.id


class Multiple_job(models.Model):
    belong_job = models.ForeignKey(job, on_delete=models.CASCADE, verbose_name="作业项目")
    belong_question = models.ForeignKey(Multiple_Choice, on_delete=models.CASCADE, related_name=None, verbose_name="题目")

    class Meta:
        ordering = ['id']
        verbose_name = '题目'
        verbose_name_plural = '多选题目'

    def __init(self):
        return self.id


class Judge_job(models.Model):
    belong_job = models.ForeignKey(job, on_delete=models.CASCADE, verbose_name="作业项目")
    belong_question = models.ForeignKey(Judge, on_delete=models.CASCADE, related_name=None, verbose_name="题目")

    class Meta:
        ordering = ['id']
        verbose_name = '题目'
        verbose_name_plural = '判断题目'

    def __init(self):
        return self.id


class Results_job(models.Model):
    TYPE_CHOICES = (
        ('评分', '评分'),
        ('理论', '理论')
    )

    belong_contestList = models.ForeignKey(contestList, on_delete=models.CASCADE, verbose_name="竞赛")
    belong_job = models.ForeignKey(job, on_delete=models.CASCADE, verbose_name="作业项目", null=True, blank=True)
    sid = models.ForeignKey(Students, on_delete=models.CASCADE, related_name=None, verbose_name="学生名字")
    score = models.DecimalField(verbose_name='分数', decimal_places=1, max_digits=5)
    submit = models.DateTimeField("提交时间", auto_now_add=True)
    type = models.CharField(verbose_name='类型', max_length=10, choices=TYPE_CHOICES, default='理论')

    class Meta:
        ordering = ['id']
        verbose_name = '成绩'
        verbose_name_plural = '学生成绩'

    def __init(self):
        return self.id


class Choice_res(models.Model):
    belong_contestList = models.ForeignKey(contestList, on_delete=models.CASCADE, verbose_name="竞赛", null=True,
                                           blank=True)
    belong_job = models.ForeignKey(job, on_delete=models.CASCADE, verbose_name="作业项目", null=True, blank=True)
    belong_question = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name=None, verbose_name="题目")
    isscore = models.BooleanField("得分", default=False)
    score = models.DecimalField(verbose_name='分值', decimal_places=2, max_digits=5, null=True, blank=True)
    answer = models.CharField("答题", max_length=10)
    sid = models.ForeignKey(Students, on_delete=models.CASCADE, related_name=None, verbose_name="学生名字")

    class Meta:
        ordering = ['id']
        verbose_name = '选择题记录'
        verbose_name_plural = '选择题记录'

    def __init(self):
        return self.id


class Multiple_res(models.Model):
    belong_contestList = models.ForeignKey(contestList, on_delete=models.CASCADE, verbose_name="竞赛", null=True,
                                           blank=True)
    belong_job = models.ForeignKey(job, on_delete=models.CASCADE, verbose_name="作业项目", null=True, blank=True)
    belong_question = models.ForeignKey(Multiple_Choice, on_delete=models.CASCADE, related_name=None, verbose_name="题目")
    isscore = models.BooleanField("得分", default=False)
    score = models.DecimalField(verbose_name='分值', decimal_places=2, max_digits=5, null=True, blank=True)
    answer = models.CharField("答题", max_length=10)
    sid = models.ForeignKey(Students, on_delete=models.CASCADE, related_name=None, verbose_name="学生名字")

    class Meta:
        ordering = ['id']
        verbose_name = '多选题记录'
        verbose_name_plural = verbose_name

    def __init(self):
        return self.id


class Judge_res(models.Model):
    belong_contestList = models.ForeignKey(contestList, on_delete=models.CASCADE, verbose_name="竞赛", null=True,
                                           blank=True)
    belong_job = models.ForeignKey(job, on_delete=models.CASCADE, verbose_name="作业项目", null=True, blank=True)
    belong_question = models.ForeignKey(Judge, on_delete=models.CASCADE, related_name=None, verbose_name="题目")
    isscore = models.BooleanField("得分", default=False)
    score = models.DecimalField(verbose_name='分值', decimal_places=2, max_digits=5, null=True, blank=True)
    answer = models.CharField("答题", max_length=10)
    sid = models.ForeignKey(Students, on_delete=models.CASCADE, related_name=None, verbose_name="学生名字")

    class Meta:
        ordering = ['id']
        verbose_name = '判断题记录'
        verbose_name_plural = verbose_name

    def __init(self):
        return self.id


class Merge(models.Model):
    TYPE_CHOICES = (
        ('表格', '表格'),
        ('理论', '理论')
    )
    belong_contestList = models.ForeignKey(contestList, on_delete=models.CASCADE, verbose_name="竞赛", null=True,
                                           blank=True)
    sid = models.ForeignKey(Students, on_delete=models.CASCADE, related_name=None, verbose_name="学生名字")
    score = models.DecimalField(verbose_name='分数', decimal_places=2, max_digits=5, null=True, blank=True)
    teacher = models.ForeignKey(Teachers, on_delete=models.CASCADE, verbose_name="裁判")
    submit = models.DateTimeField("提交时间", auto_now_add=True)
    type = models.CharField(verbose_name='类型', max_length=10, choices=TYPE_CHOICES, default='理论')

    class Meta:
        ordering = ['id']
        verbose_name = '总成绩'
        verbose_name_plural = verbose_name

    def __init(self):
        return self.id
