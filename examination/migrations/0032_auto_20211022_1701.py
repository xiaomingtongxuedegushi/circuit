# Generated by Django 3.1.6 on 2021-10-22 09:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examination', '0031_auto_20211022_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examinations',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 22, 17, 1, 53, 21510), verbose_name='结束时间'),
        ),
        migrations.AlterField(
            model_name='examinations',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 22, 17, 1, 53, 21510), verbose_name='开始时间'),
        ),
    ]
