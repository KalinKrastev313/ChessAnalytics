# Generated by Django 4.2.2 on 2023-08-31 15:08

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fenreader', '0019_customgames'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomGame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_position', models.CharField(blank=True, null=True, validators=[django.core.validators.RegexValidator('[\\d/pnbrqkPNBRQK]+ [wb] [QKqk\\-]{1,4} [\\-a-h1-8]{1,2} [\\d]{1,2} [\\d]{1,2}')])),
                ('moves_pgn', models.CharField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='CustomGames',
        ),
    ]
