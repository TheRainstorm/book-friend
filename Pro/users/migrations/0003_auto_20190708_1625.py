# Generated by Django 2.2.3 on 2019-07-08 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20190706_1534'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(default='male', max_length=10, verbose_name='性别'),
        ),
        migrations.AddField(
            model_name='user',
            name='signature',
            field=models.CharField(default='', max_length=100, verbose_name='个性签名'),
        ),
        migrations.RemoveField(
            model_name='user',
            name='recent_read',
        ),
        migrations.AddField(
            model_name='user',
            name='recent_read',
            field=models.CharField(default='[]', max_length=100, verbose_name='最近浏览'),
        ),
    ]
