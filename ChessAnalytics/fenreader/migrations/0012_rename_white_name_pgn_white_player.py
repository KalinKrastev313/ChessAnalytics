# Generated by Django 4.2.2 on 2023-08-16 11:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fenreader', '0011_pgn'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pgn',
            old_name='white_name',
            new_name='white_player',
        ),
    ]
