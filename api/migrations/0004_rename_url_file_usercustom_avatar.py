# Generated by Django 4.2.7 on 2023-11-21 05:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_rename_avatar_usercustom_url_file'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usercustom',
            old_name='url_file',
            new_name='avatar',
        ),
    ]