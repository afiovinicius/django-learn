# Generated by Django 4.2.7 on 2023-12-26 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_rename_url_file_usercustom_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='month',
            field=models.CharField(default='December'),
        ),
    ]
