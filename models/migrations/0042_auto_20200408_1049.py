# Generated by Django 3.0.5 on 2020-04-08 15:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0041_auto_20200408_1042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskitem',
            name='task_created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 8, 10, 49, 21, 361598)),
        ),
        migrations.AlterField(
            model_name='taskitem',
            name='task_due_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 8, 10, 49, 21, 361620)),
        ),
    ]
