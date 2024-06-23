# Generated by Django 4.0 on 2024-04-06 13:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserVisit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visit_time', models.DateTimeField(verbose_name='访问时间')),
                ('rating', models.FloatField(verbose_name='评分')),
                ('data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.data', verbose_name='菜品')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user', verbose_name='用户')),
            ],
            options={
                'verbose_name': '用户访问记录',
                'verbose_name_plural': '用户访问记录',
            },
        ),
    ]