# Generated by Django 3.1.6 on 2021-10-20 08:04

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usermanage', '0001_initial'),
        ('examination', '0022_auto_20211018_2219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examinations',
            name='belong_te',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='be_te', to='usermanage.teachers', verbose_name='教师'),
        ),
        migrations.AlterField(
            model_name='examinations',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 20, 16, 4, 47, 573819), verbose_name='结束时间'),
        ),
        migrations.AlterField(
            model_name='examinations',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 20, 16, 4, 47, 572816), verbose_name='开始时间'),
        ),
    ]
