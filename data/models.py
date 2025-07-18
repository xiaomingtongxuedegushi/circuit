from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Userinfo(models.Model):
    belong_user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    identity = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['id']
        verbose_name = '用户名'
        verbose_name_plural = '用户身份管理'

    def __str__(self):
        return self.belong_user


class Classification(models.Model):
    class_name = models.CharField("车型名称", max_length=10, blank=True, null=True)

    class Meta:
        ordering = ['id']
        verbose_name = '车型名称'
        verbose_name_plural = '车型管理'

    def __str__(self):
        return self.class_name


class Fault(models.Model):
    STATUS_CHOICES = (
        (0, '正常'),
        (1, '故障'),
        (2, '断路'),
    )

    name = models.CharField("故障名", max_length=20, blank=True, null=True)
    card = models.IntegerField("板卡号", null=True, blank=True)
    address = models.IntegerField("故障地址", null=True, blank=True)
    status = models.IntegerField("当前状态", null=True, blank=True,choices=STATUS_CHOICES)
    belong_class = models.ForeignKey(Classification, on_delete=models.SET_NULL, related_name='fault_class', null=True,
                                     blank=True, verbose_name="车型")
                                    #   default=Classification.objects.all()[0].id

    class Meta:
        ordering = ['id']
        verbose_name = '故障名称'
        verbose_name_plural = '故障设置'

    def __str__(self):
        return self.name


class serial(models.Model):
    name = models.CharField("名称",max_length=10)
    port = models.IntegerField("端口号")
    class Meta:
        verbose_name = '串口配置'
        verbose_name_plural = verbose_name

        def __init(self):
            return self.port