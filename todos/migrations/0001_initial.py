# Generated by Django 5.0.7 on 2024-09-16 11:21

import django.db.models.deletion
import todos.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('done', 'DONE'), ('not_yet', 'NOT_YET')], default=todos.models.TodoStatus['NOT_YET'], help_text='완료 상태', max_length=10)),
                ('title', models.CharField(max_length=64)),
                ('content', models.TextField(blank=True)),
                ('due_date', models.DateTimeField(help_text='마감 기한')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
