# Generated by Django 3.1.6 on 2021-10-14 15:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examination', '0016_auto_20211014_2342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examinations',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 14, 23, 54, 46, 676705), verbose_name='结束时间'),
        ),
        migrations.AlterField(
            model_name='examinations',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 14, 23, 54, 46, 676705), verbose_name='开始时间'),
        ),
    ]
