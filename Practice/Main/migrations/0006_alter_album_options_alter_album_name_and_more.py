# Generated by Django 5.0.6 on 2024-06-29 08:12

import Main.untils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0005_album'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='album',
            options={'ordering': ['year'], 'verbose_name': 'Альбом', 'verbose_name_plural': 'Альбомы'},
        ),
        migrations.AlterField(
            model_name='album',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Альбом'),
        ),
        migrations.AlterField(
            model_name='album',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to=Main.untils.album_directory_path, verbose_name='Изображение'),
        ),
    ]