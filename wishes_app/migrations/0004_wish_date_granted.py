# Generated by Django 2.2 on 2021-07-16 08:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wishes_app', '0003_wish_granted'),
    ]

    operations = [
        migrations.AddField(
            model_name='wish',
            name='date_granted',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 16, 1, 28, 19, 632481)),
            preserve_default=False,
        ),
    ]
