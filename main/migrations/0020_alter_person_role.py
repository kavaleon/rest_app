# Generated by Django 5.1.4 on 2025-02-20 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_alter_grade_time_create'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='role',
            field=models.CharField(default='0', max_length=7, verbose_name='права'),
        ),
    ]
