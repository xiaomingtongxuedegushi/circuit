# Generated by Django 3.1.6 on 2021-10-08 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0004_auto_20211008_1823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='criteria',
            name='judge_answer',
            field=models.IntegerField(blank=True, choices=[(1, '正常'), (2, '维修'), (3, '更换'), (4, '调整')], null=True, verbose_name='判断正确值'),
        ),
    ]
