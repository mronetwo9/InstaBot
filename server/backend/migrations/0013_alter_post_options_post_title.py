# Generated by Django 4.0.3 on 2022-03-25 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0012_post'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'verbose_name': 'Публикация', 'verbose_name_plural': 'Публикации'},
        ),
        migrations.AddField(
            model_name='post',
            name='title',
            field=models.CharField(default='', max_length=255, verbose_name='Название(для себя)'),
            preserve_default=False,
        ),
    ]
