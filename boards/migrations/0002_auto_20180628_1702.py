# Generated by Django 2.0.6 on 2018-06-28 09:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='topic',
            old_name='话题排序',
            new_name='last_updated',
        ),
    ]
