# Generated by Django 5.0.6 on 2024-06-29 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0008_track_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Название'),
        ),
    ]