# Generated by Django 5.1.4 on 2024-12-27 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_grade_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='image',
            field=models.ImageField(default='', upload_to='photos/%Y/%m/%d'),
        ),
    ]
