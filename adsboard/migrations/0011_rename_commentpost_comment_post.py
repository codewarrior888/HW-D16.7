# Generated by Django 5.0.4 on 2024-04-29 00:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adsboard', '0010_rename_comment_post_comment_commentpost_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='commentpost',
            new_name='post',
        ),
    ]
