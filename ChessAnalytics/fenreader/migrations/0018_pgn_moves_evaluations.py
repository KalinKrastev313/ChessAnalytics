# Generated by Django 4.2.2 on 2023-08-18 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fenreader', '0017_alter_engineline_evaluation'),
    ]

    operations = [
        migrations.AddField(
            model_name='pgn',
            name='moves_evaluations',
            field=models.TextField(blank=True, null=True),
        ),
    ]
