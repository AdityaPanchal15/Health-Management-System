# Generated by Django 2.2.10 on 2020-04-20 07:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health', '0005_auto_20200417_0857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='date',
            field=models.DateField(default=datetime.date(2020, 4, 20)),
        ),
    ]
