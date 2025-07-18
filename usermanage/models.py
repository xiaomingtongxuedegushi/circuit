from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Department(models.Model):
    de_name = models.CharField("院系名称", max_length=50, null=True, blank=True)

    class Meta:
        ordering = ['id']
        verbose_name = '院系名称'
        verbose_name_plural = '院系管理'

    def __str__(self):
        return self.de_name


class Classes(models.Model):
    cl_name = models.CharField("班级名称", max_length=50)
    belong_De = models.ForeignKey(Department, on_delete=models.SET_NULL, related_name="be_De", null=True, blank=True,
                                  verbose_name="所属院系")

    class Meta:
        ordering = ['id']
        verbose_name = '班级名称'
        verbose_name_plural = '班级管理'

    def __str__(self):
        return self.cl_name


class Students(models.Model):
    SEX = (
        ('男', '男'),
        ('女', '女'),
    )

    sid = models.IntegerField("学号")
    password = models.CharField("密码", max_length=50, default="qichezhinengyitihua")
    name = models.CharField("姓名", max_length=50)
    sex = models.CharField("性别", max_length=4, choices=SEX, default="男")
    belong_class = models.ForeignKey(Classes, on_delete=models.SET_NULL, related_name="be_Cl", verbose_name="所在班级",
                                     null=True, blank=True)

    class Meta:
        ordering = ['id']
        verbose_name = '学生名字'
        verbose_name_plural = '学生管理'

    def __str__(self):
        return self.name

class Teachers(models.Model):
    SEX = (
        ('男', '男'),
        ('女', '女'),
    )
    enable = models.BooleanField("启用", default=False)
    tid = models.CharField("教工号", max_length=50, primary_key=True)
    password = models.CharField("密码", max_length=50, default="qichezhinengyitihua",editable=False)
    name = models.CharField('姓名', max_length=50)
    sex = models.CharField('性别', max_length=4, choices=SEX, default='男')
    belong_De = models.ForeignKey(Department, on_delete=models.SET_NULL, related_name="be_Dep", null=True, blank=True,
                                  verbose_name="所属院系")
    belong_user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="关联用户")

    class Meta:
        verbose_name = '教师名称'
        verbose_name_plural = '教师管理'

    def __str__(self):
        return self.name
