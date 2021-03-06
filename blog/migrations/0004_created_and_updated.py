# Generated by Django 2.2.16 on 2020-09-06 00:23 and modified by kaj

from django.db import migrations, models
import django.utils.timezone


def set_my_defaults(apps, schema_editor):
    Post = apps.get_model('blog', 'post')
    for post in Post.objects.all().iterator():
        posted_or_now = post.posted_time or django.utils.timezone.now()
        post.updated_at = posted_or_now
        post.created_at = posted_or_now
        post.save()

def reverse_my_defaults(apps, schema_editor):
    pass  # No need to do anything, the fields will be removed.

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20180102_2318'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(null=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='updated_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.RunPython(set_my_defaults, reverse_my_defaults),
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
