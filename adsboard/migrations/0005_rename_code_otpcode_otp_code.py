# Generated by Django 5.0.4 on 2024-04-25 05:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adsboard', '0004_rename_post_comment_comment_post_delete_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='otpcode',
            old_name='code',
            new_name='otp_code',
        ),
    ]