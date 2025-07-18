from django.db import models
from data.models import Classification
from multiselectfield import MultiSelectField


# Create your models here.
class QuestionType(models.Model):
    question_type = models.CharField("题目类型", max_length=20, null=True, blank=True)

    class Meta:
        ordering = ['id']
        verbose_name = '题目类型'
        verbose_name_plural = '题目类型管理'

    def __str__(self):
        return self.question_type


class Choice(models.Model):
    """选择题模型"""
    LEVEL_CHOICES = (
        ('1', '入门'),
        ('2', '简单'),
        ('3', '普通'),
        ('4', '较难'),
        ('5', '困难')
    )
    ANSWER_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D')
    )

    TYPE_CHOICES = (
        (0, '自建'),
        (1, '官方')
    )
    question = models.TextField("题目", default="")
    images = models.ImageField("图片", upload_to='choice/', null=True, blank=True)
    answer_A = models.CharField("A选项", max_length=200, default="")
    answer_B = models.CharField("B选项", max_length=200, default="")
    answer_C = models.CharField("C选项", max_length=200, default="")
    answer_D = models.CharField("D选项", max_length=200, default="")
    right_answer = models.CharField("正确选项", max_length=1, choices=ANSWER_CHOICES, default="A")
    score =  models.DecimalField(verbose_name='分值', decimal_places=2, max_digits=5, default='2', null=True, blank=True)
    analysis = models.TextField("题目解析", default="暂无")
    level = models.CharField("难度等级", max_length=1, choices=LEVEL_CHOICES, default='1')
    belong_class = models.ForeignKey(Classification, on_delete=models.SET_DEFAULT, related_name='Choice_class',
                                     null=True,
                                     blank=True, verbose_name="车型", default=Classification.objects.all()[0].id)
    belong_type = models.ForeignKey(QuestionType, on_delete=models.SET_DEFAULT, related_name='Choice_Type', null=True,
                                    blank=True, verbose_name="题目类型", default=QuestionType.objects.all()[0].id)

    remarks = models.CharField("备注", max_length=200, null=True, blank=True)
    type = models.IntegerField("题库", choices=TYPE_CHOICES, default=0)

    class Meta:
        ordering = ['id']
        verbose_name = '选择题'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.question


class Multiple_Choice(models.Model):
    """多选题模型"""
    LEVEL_CHOICES = (
        ('1', '入门'),
        ('2', '简单'),
        ('3', '普通'),
        ('4', '较难'),
        ('5', '困难')
    )
    TYPE_CHOICES = (
        (0, '自建'),
        (1, '官方')
    )
    # ANSWER_CHOICES = (
    #     ('A,B', 'A,B'),
    #     ('A,B,C', 'A,B,C'),
    #     ('A,B,C,D', 'A,B,C,D'),
    #     ('B,C', 'B,C'),
    #     ('B,D', 'B,D'),
    #     ('B,C,D', 'B,C,D'),
    #     ('C,D', 'C,D'),
    #     ('A,C', 'A,C'),
    #     ('A,C,D', 'A,C,D'),
    #     ('A,B,D', 'A,B,D'),
    #     ('A,D', 'A,D'),
    #
    # )
    ACHOICE = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D')
    )
    question = models.TextField("题目", default="")
    images = models.ImageField("图片", upload_to='multiple/', null=True, blank=True)
    answer_A = models.CharField("A选项", max_length=200, default="")
    answer_B = models.CharField("B选项", max_length=200, default="")
    answer_C = models.CharField("C选项", max_length=200, default="")
    answer_D = models.CharField("D选项", max_length=200, default="")
    right_answer = MultiSelectField("正确选项", choices=ACHOICE, default='A')
    score =  models.DecimalField(verbose_name='分值', decimal_places=2, max_digits=5, default='2', null=True, blank=True)
    analysis = models.TextField("题目解析", default="暂无")
    level = models.CharField("难度等级", max_length=1, choices=LEVEL_CHOICES, default='1')
    belong_class = models.ForeignKey(Classification, on_delete=models.SET_DEFAULT, related_name='Multiple_class',
                                     verbose_name="车型",
                                     default=Classification.objects.all()[0].id)
    belong_type = models.ForeignKey(QuestionType, on_delete=models.SET_DEFAULT, related_name='Multiple_Type',
                                    verbose_name="题目类型", default=QuestionType.objects.all()[0].id)
    remarks = models.CharField("备注", max_length=200, null=True, blank=True)
    type = models.IntegerField("题库", choices=TYPE_CHOICES, default=0)

    class Meta:
        ordering = ['id']
        verbose_name = '多选题'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.question


class Judge(models.Model):
    """判断题模型"""
    LEVEL_CHOICES = (
        ('1', '入门'),
        ('2', '简单'),
        ('3', '普通'),
        ('4', '较难'),
        ('5', '困难')
    )
    ANSWER_CHOICES = (
        ('T', '正确'),
        ('F', '错误')
    )
    TYPE_CHOICES = (
        (0, '自建'),
        (1, '官方')
    )
    question = models.TextField("题目", default="")
    images = models.ImageField("图片", upload_to='judge/', null=True, blank=True)
    right_answer = models.CharField("正确答案", max_length=1, choices=ANSWER_CHOICES, default="T")
    score =  models.DecimalField(verbose_name='分值', decimal_places=2, max_digits=5, default='2', null=True, blank=True)
    analysis = models.TextField("题目解析", default="暂无")
    level = models.CharField("难度等级", max_length=1, choices=LEVEL_CHOICES, default='1')
    belong_class = models.ForeignKey(Classification, on_delete=models.SET_DEFAULT, related_name='Judge_class',
                                     verbose_name="车型", default=Classification.objects.all()[0].id)
    belong_type = models.ForeignKey(QuestionType, on_delete=models.SET_DEFAULT, related_name='Judge_Type',
                                    verbose_name="题目类型", default=QuestionType.objects.all()[0].id)
    remarks = models.CharField("备注", max_length=200, null=True, blank=True)
    type = models.IntegerField("题库", choices=TYPE_CHOICES, default=0)

    class Meta:
        ordering = ['id']
        verbose_name = '判断题'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.question
