# Generated by Django 3.2.12 on 2023-04-13 08:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0002_auto_20230412_1032'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='full_name',
            new_name='name',
        ),
    ]
