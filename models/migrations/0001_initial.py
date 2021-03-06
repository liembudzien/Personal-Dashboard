# Generated by Django 3.0.5 on 2020-04-22 16:19

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TaskList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_list_name', models.CharField(default='To Do List', max_length=100)),
                ('task_list_description', models.CharField(default='My To Do List', max_length=100)),
                ('task_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='models.Profile')),
            ],
            options={
                'ordering': ['task_list_name'],
            },
        ),
        migrations.CreateModel(
            name='TaskItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(default='Task', max_length=100)),
                ('tast_description', models.CharField(default='Task Description', max_length=100)),
                ('task_created_date', models.DateTimeField(default=datetime.datetime(2020, 4, 22, 11, 19, 49, 976698))),
                ('task_due_date', models.DateTimeField(default=datetime.datetime(2020, 4, 22, 11, 19, 49, 976717))),
                ('task_priority', models.IntegerField(choices=[(1, 'low'), (2, 'normal'), (3, 'high')], default=1)),
                ('task_completion', models.BooleanField(default=False)),
                ('task_list', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='models.TaskList')),
            ],
            options={
                'ordering': ['task_due_date'],
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('city_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='models.Profile')),
            ],
            options={
                'verbose_name_plural': 'cities',
            },
        ),
    ]
