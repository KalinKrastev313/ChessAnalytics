# Generated by Django 4.2.2 on 2023-08-18 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fenreader', '0015_alter_pgn_pgn_moves'),
    ]

    operations = [
        migrations.AddField(
            model_name='engineline',
            name='is_mate',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]