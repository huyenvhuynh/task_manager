# Generated by Django 5.1.1 on 2024-12-05 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0005_alter_assignmentfile_assignment_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='keywords',
        ),
        migrations.AddField(
            model_name='assignmentfile',
            name='keywords',
            field=models.CharField(blank=True, help_text='Comma-separated keywords', max_length=255, null=True),
        ),
    ]
