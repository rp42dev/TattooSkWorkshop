# Generated by Django 4.1.3 on 2022-11-28 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0017_alter_about_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='about',
            name='order',
            field=models.IntegerField(default=424),
        ),
    ]