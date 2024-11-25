# Generated by Django 5.1.2 on 2024-11-25 13:11

import datetime
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sdpApp', '0004_blogdesc_category_content_activitylog_blog_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogdesc',
            name='category_id',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='blog_desc',
        ),
        migrations.DeleteModel(
            name='Content',
        ),
        migrations.AddField(
            model_name='blog',
            name='blog_title',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='blog',
            name='category_name',
            field=models.CharField(default='', max_length=100, unique=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='blog',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='blog',
            name='text',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='blog',
            name='time',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='BlogDesc',
        ),
    ]
