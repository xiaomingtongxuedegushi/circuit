# Generated by Django 3.1.6 on 2021-10-20 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanage', '0002_teachers_en'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teachers',
            name='en',
        ),
        migrations.AddField(
            model_name='teachers',
            name='enable',
            field=models.BooleanField(default=True, verbose_name='启用'),
        ),
    ]
