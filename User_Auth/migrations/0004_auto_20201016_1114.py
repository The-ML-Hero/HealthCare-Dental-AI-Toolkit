# Generated by Django 3.1.2 on 2020-10-16 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_Auth', '0003_auto_20201016_1112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verify_f',
            name='verification_code',
            field=models.TextField(max_length=30),
        ),
    ]
