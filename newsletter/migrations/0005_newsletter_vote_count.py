# Generated by Django 3.2 on 2022-01-30 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0004_auto_20220129_0533'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsletter',
            name='vote_count',
            field=models.IntegerField(default=0),
        ),
    ]
