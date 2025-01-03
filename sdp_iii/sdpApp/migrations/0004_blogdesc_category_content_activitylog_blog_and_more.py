# Generated by Django 5.1.2 on 2024-11-18 14:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sdpApp', '0003_login'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogDesc',
            fields=[
                ('blog_desc_id', models.AutoField(primary_key=True, serialize=False)),
                ('blog_desc_title', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('content_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False)),
                ('category_name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('content_id', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.TextField()),
                ('image', models.ImageField(null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('log_id', models.AutoField(primary_key=True, serialize=False)),
                ('action_type', models.CharField(choices=[('post_blog', 'Post Blog'), ('delete_comment', 'Delete Comment'), ('like', 'Like'), ('share', 'Share'), ('login', 'Login'), ('logout', 'Logout')], max_length=50)),
                ('date_time', models.DateTimeField()),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('blog_id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('published', 'Published'), ('draft', 'Draft'), ('archived', 'Archived')], default='draft', max_length=10)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('blog_desc', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sdpApp.blogdesc')),
            ],
        ),
        migrations.AddField(
            model_name='blogdesc',
            name='category_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sdpApp.category'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment_id', models.AutoField(primary_key=True, serialize=False)),
                ('comments', models.TextField()),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('status', models.CharField(choices=[('visible', 'Visible'), ('hidden', 'Hidden')], default='visible', max_length=10)),
                ('blog_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sdpApp.blog')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('reaction_id', models.AutoField(primary_key=True, serialize=False)),
                ('reaction_type', models.CharField(choices=[('like', 'Like'), ('love', 'Love'), ('laugh', 'Laugh'), ('angry', 'Angry')], max_length=10)),
                ('blog_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sdpApp.blog')),
                ('comment_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sdpApp.comment')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user_id', 'blog_id', 'comment_id')},
            },
        ),
    ]
