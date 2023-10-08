# Generated by Django 4.2.5 on 2023-10-07 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_manager', '0009_commentary'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='is_need_help',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High'), ('URGENT', 'Urgent'), ('CRITICAL', 'Critical')], max_length=8),
        ),
    ]
