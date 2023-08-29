# Generated by Django 4.2.2 on 2023-08-29 11:29

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fenreader', '0018_pgn_moves_evaluations'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomGames',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_position', models.CharField(blank=True, default='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', validators=[django.core.validators.RegexValidator('[\\d/pnbrqkPNBRQK]+ [wb] [QKqk\\-]{1,4} [\\-a-h1-8]{1,2} [\\d]{1,2} [\\d]{1,2}')])),
                ('moves_pgn', models.CharField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
