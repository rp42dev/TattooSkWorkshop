# Generated by Django 3.2.7 on 2022-11-15 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0010_alter_about_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='about',
            name='order',
            field=models.IntegerField(default=965),
        ),
    ]
