# Generated by Django 3.1.6 on 2021-02-27 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0012_auto_20210227_1043'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='prosmotr',
            field=models.IntegerField(default=0),
        ),
    ]
