# Generated by Django 5.0.4 on 2024-04-29 05:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adsboard', '0012_comment_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='parent',
        ),
    ]
