# Generated by Django 3.1.6 on 2021-10-04 09:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examination', '0006_auto_20211002_2235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examinations',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 4, 17, 0, 45, 590151), verbose_name='结束时间'),
        ),
        migrations.AlterField(
            model_name='examinations',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 4, 17, 0, 45, 590151), verbose_name='开始时间'),
        ),
    ]
