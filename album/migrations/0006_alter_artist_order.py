# Generated by Django 3.2.7 on 2022-11-15 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0005_auto_20221107_2020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='order',
            field=models.IntegerField(default=1),
        ),
    ]
