# Generated by Django 4.2.7 on 2023-11-21 05:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_usercustom_is_active_usercustom_is_staff_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usercustom',
            old_name='avatar',
            new_name='url_file',
        ),
    ]
