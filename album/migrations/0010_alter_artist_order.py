# Generated by Django 4.1.3 on 2022-11-18 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0009_alter_artist_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='order',
            field=models.IntegerField(default=1),
        ),
    ]
