# Generated by Django 4.2.2 on 2023-08-06 08:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fenreader', '0003_fenposition_black_player_fenposition_tournament_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='fenposition',
            name='black_rating',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(800), django.core.validators.MaxValueValidator(4000)]),
        ),
        migrations.AddField(
            model_name='fenposition',
            name='white_rating',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(800), django.core.validators.MaxValueValidator(4000)]),
        ),
    ]