# Generated by Django 3.1.2 on 2020-10-20 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CBCT_Model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CBCT_name', models.CharField(max_length=250)),
                ('CBCT_file', models.FileField(upload_to='images/root_segmentation')),
                ('CBCT_image', models.ImageField(upload_to='')),
                ('date_uploaded_CBCT', models.DateField(auto_now=True)),
            ],
        ),
    ]
