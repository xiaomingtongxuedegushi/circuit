# Generated by Django 3.1.6 on 2021-10-02 06:56

from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_type', models.CharField(blank=True, max_length=20, null=True, verbose_name='题目类型')),
            ],
            options={
                'verbose_name': '题目类型',
                'verbose_name_plural': '题目类型管理',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Multiple_Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(default='', verbose_name='题目')),
                ('images', models.ImageField(blank=True, null=True, upload_to='multiple/', verbose_name='图片')),
                ('answer_A', models.CharField(default='', max_length=200, verbose_name='A选项')),
                ('answer_B', models.CharField(default='', max_length=200, verbose_name='B选项')),
                ('answer_C', models.CharField(default='', max_length=200, verbose_name='C选项')),
                ('answer_D', models.CharField(default='', max_length=200, verbose_name='D选项')),
                ('right_answer', multiselectfield.db.fields.MultiSelectField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], default='A', max_length=7, verbose_name='正确选项')),
                ('score', models.DecimalField(blank=True, decimal_places=2, default='2', max_digits=5, null=True, verbose_name='分值')),
                ('analysis', models.TextField(default='暂无', verbose_name='题目解析')),
                ('level', models.CharField(choices=[('1', '入门'), ('2', '简单'), ('3', '普通'), ('4', '较难'), ('5', '困难')], default='1', max_length=1, verbose_name='难度等级')),
                ('remarks', models.CharField(blank=True, max_length=200, null=True, verbose_name='备注')),
                ('type', models.IntegerField(choices=[(0, '自建'), (1, '官方')], default=0, verbose_name='题库')),
                ('belong_class', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='Multiple_class', to='data.classification', verbose_name='车型')),
                ('belong_type', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='Multiple_Type', to='question.questiontype', verbose_name='题目类型')),
            ],
            options={
                'verbose_name': '多选题',
                'verbose_name_plural': '多选题',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Judge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(default='', verbose_name='题目')),
                ('images', models.ImageField(blank=True, null=True, upload_to='judge/', verbose_name='图片')),
                ('right_answer', models.CharField(choices=[('T', '正确'), ('F', '错误')], default='T', max_length=1, verbose_name='正确答案')),
                ('score', models.DecimalField(blank=True, decimal_places=2, default='2', max_digits=5, null=True, verbose_name='分值')),
                ('analysis', models.TextField(default='暂无', verbose_name='题目解析')),
                ('level', models.CharField(choices=[('1', '入门'), ('2', '简单'), ('3', '普通'), ('4', '较难'), ('5', '困难')], default='1', max_length=1, verbose_name='难度等级')),
                ('remarks', models.CharField(blank=True, max_length=200, null=True, verbose_name='备注')),
                ('type', models.IntegerField(choices=[(0, '自建'), (1, '官方')], default=0, verbose_name='题库')),
                ('belong_class', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='Judge_class', to='data.classification', verbose_name='车型')),
                ('belong_type', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='Judge_Type', to='question.questiontype', verbose_name='题目类型')),
            ],
            options={
                'verbose_name': '判断题',
                'verbose_name_plural': '判断题',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(default='', verbose_name='题目')),
                ('images', models.ImageField(blank=True, null=True, upload_to='choice/', verbose_name='图片')),
                ('answer_A', models.CharField(default='', max_length=200, verbose_name='A选项')),
                ('answer_B', models.CharField(default='', max_length=200, verbose_name='B选项')),
                ('answer_C', models.CharField(default='', max_length=200, verbose_name='C选项')),
                ('answer_D', models.CharField(default='', max_length=200, verbose_name='D选项')),
                ('right_answer', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], default='A', max_length=1, verbose_name='正确选项')),
                ('score', models.DecimalField(blank=True, decimal_places=2, default='2', max_digits=5, null=True, verbose_name='分值')),
                ('analysis', models.TextField(default='暂无', verbose_name='题目解析')),
                ('level', models.CharField(choices=[('1', '入门'), ('2', '简单'), ('3', '普通'), ('4', '较难'), ('5', '困难')], default='1', max_length=1, verbose_name='难度等级')),
                ('remarks', models.CharField(blank=True, max_length=200, null=True, verbose_name='备注')),
                ('type', models.IntegerField(choices=[(0, '自建'), (1, '官方')], default=0, verbose_name='题库')),
                ('belong_class', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='Choice_class', to='data.classification', verbose_name='车型')),
                ('belong_type', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='Choice_Type', to='question.questiontype', verbose_name='题目类型')),
            ],
            options={
                'verbose_name': '选择题',
                'verbose_name_plural': '选择题',
                'ordering': ['id'],
            },
        ),
    ]
