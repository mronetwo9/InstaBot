# Generated by Django 4.0.3 on 2022-03-19 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='botuser',
            name='full_name',
            field=models.CharField(default='', max_length=255, verbose_name='Полное имя'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='botuser',
            name='username',
            field=models.CharField(default='', max_length=255, verbose_name='Юзернейм'),
            preserve_default=False,
        ),
    ]
