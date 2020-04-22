# Generated by Django 3.0.2 on 2020-04-20 12:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cfis', '0003_auto_20200418_1439'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fave',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cfis.Post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('post', 'user')},
            },
        ),
        migrations.AddField(
            model_name='post',
            name='favorites',
            field=models.ManyToManyField(related_name='favorite_post', through='cfis.Fave', to=settings.AUTH_USER_MODEL),
        ),
    ]
