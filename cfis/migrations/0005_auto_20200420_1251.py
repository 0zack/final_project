# Generated by Django 3.0.2 on 2020-04-20 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cfis', '0004_auto_20200420_1218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(to='cfis.Tag'),
        ),
    ]
