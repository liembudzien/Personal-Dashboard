# Generated by Django 3.0.5 on 2020-04-28 03:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0011_auto_20200427_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskitem',
            name='task_created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 27, 22, 28, 29, 310072)),
        ),
        migrations.AlterField(
            model_name='taskitem',
            name='task_due_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 27, 22, 28, 29, 310096)),
        ),
    ]
