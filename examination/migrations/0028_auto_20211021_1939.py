# Generated by Django 3.1.6 on 2021-10-21 11:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examination', '0027_auto_20211021_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examinations',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 21, 19, 39, 33, 486774), verbose_name='结束时间'),
        ),
        migrations.AlterField(
            model_name='examinations',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 21, 19, 39, 33, 486774), verbose_name='开始时间'),
        ),
    ]
