# Generated by Django 2.2.3 on 2019-07-06 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('user_id', models.AutoField(primary_key=True, serialize=False, verbose_name='用户的id')),
                ('image', models.URLField()),
                ('user_name', models.CharField(max_length=20, unique=True, verbose_name='用户名称')),
                ('password', models.CharField(max_length=40, verbose_name='用户密码')),
                ('recent_read', models.ManyToManyField(to='books.Book', verbose_name='最近浏览')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]