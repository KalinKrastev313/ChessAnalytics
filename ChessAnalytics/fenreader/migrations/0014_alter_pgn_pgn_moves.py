# Generated by Django 4.2.2 on 2023-08-16 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fenreader', '0013_pgn_eco_pgn_time_control_pgn_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pgn',
            name='pgn_moves',
            field=models.TextField(),
        ),
    ]