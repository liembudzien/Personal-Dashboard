# Generated by Django 2.2.7 on 2020-04-01 15:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0002_auto_20200401_0923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskitem',
            name='task_created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 1, 10, 15, 29, 337215)),
        ),
        migrations.AlterField(
            model_name='taskitem',
            name='task_due_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 1, 10, 15, 29, 337238)),
        ),
    ]
