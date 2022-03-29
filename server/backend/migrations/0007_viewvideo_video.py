# Generated by Django 4.0.3 on 2022-03-19 11:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_alter_template_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='viewvideo',
            name='video',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='views', to='backend.video'),
            preserve_default=False,
        ),
    ]
