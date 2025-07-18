from django.db import models
from django.utils.html import format_html

from usermanage.models import Teachers, Students, Classes


# Create your models here.


class Course(models.Model):
    TYPE_CHOICES = (
        (0, '自建'),
        (1, '官方')
    )

    name = models.CharField("课程名称", max_length=50)
    enable = models.BooleanField("启用", default=False)
    images = models.ImageField("展示图", upload_to='course/', default="course/timg.jpg")
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    belong_tid = models.ForeignKey(Teachers, on_delete=models.CASCADE, related_name=None, verbose_name="教师",
                                  )
    type = models.IntegerField("类型", default=0, choices=TYPE_CHOICES, blank=True, null=True, editable=True)

    def image_data(self):
        return format_html(
            '<img src="{}" width="100px"/>',
            self.images.url,
        )

    image_data.short_description = u'当前图片'

    class Meta:
        ordering = ['id']
        verbose_name = '课程'
        verbose_name_plural = "课程管理"

    def __str__(self):
        return self.name


class Resources(models.Model):
    FILE_TYPE_CHOICES = (
        ('MP4', 'MP4'),
        ('PDF', 'PDF')
    )
    TYPE_CHOICES = (
        (0, '自建'),
        (1, '官方')
    )
    belong_course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name=None, verbose_name="课程",
                                      )
    # belong_course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name=None, verbose_name="课程")
    serial = models.IntegerField("序号")
    name = models.CharField("资源名称", max_length=50)
    file = models.FileField("文件", upload_to='file/')
    file_type = models.CharField("文件类型", max_length=10, choices=FILE_TYPE_CHOICES, default='PDF')
    type = models.IntegerField("类型", default=0,choices=TYPE_CHOICES, blank=True, null=True, editable=True)
    views = models.IntegerField("浏览量", default=0,blank=True, null=True, editable=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


    def views_html(self):
        return format_html(
            '<a href="/admin/curriculum/resources_views/?belong_resources__id__exact={}">{}</span>',
            self.id,
            self.views
        )

    views_html.short_description = u'浏览量'

    class Meta:
        ordering = ['id']
        verbose_name = '课程资源'
        verbose_name_plural = "资源管理"

    def __str__(self):
        return self.name

class Resources_views(models.Model):

    # belong_course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name=None, verbose_name="课程")
    # serial = models.IntegerField("序号")
    # name = models.CharField("资源名称", max_length=50)
    # file = models.FileField("文件", upload_to='file/')
    # views = models.IntegerField("浏览量", default=0,blank=True, null=True, editable=False)
    # create_time = models.DateTimeField(auto_now_add=True)
    # update_time = models.DateTimeField(auto_now=True)

    id = models.IntegerField("#", primary_key=True)
    belong_resources = models.ForeignKey(Resources, on_delete=models.CASCADE, related_name=None, verbose_name="资源名称")
    # sid = models.IntegerField()
    sid = models.ForeignKey(Students, on_delete=models.CASCADE, related_name=None, verbose_name="学生姓名")
    # cid = sid.(Classes, on_delete=models.CASCADE, related_name=None, verbose_name="关联班级")
    view_time = models.DateTimeField("时间", auto_now_add=True)

    belong_class = models.ForeignKey(Classes, on_delete=models.CASCADE, related_name=None, verbose_name="关联班级")

    # class_list = Classes.objects.all()


    # belong_class = sid.belong_class = models.ForeignKey(Classes, on_delete=models.CASCADE, related_name=None, verbose_name="关联班级")

    # def cla(self):
    #     aClass = Classes.objects.filter(id=self.sid.belong_class_id).first()
    #     return aClass
    # cla.short_description = u'关联班级'


    # sid = models.IntegerField("学生")
    # belong_resources_id = models.IntegerField("资源ID")


    class Meta:
        ordering = ['id']
        verbose_name = '资源记录'
        verbose_name_plural = "资源管理记录"

    def __str__(self):
        return str(self.id)