from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse

from Main.untils import ModelMixinData, band_directory_path, album_directory_path, track_directory_path
from datetime import datetime


class PublishedBandManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(ready=Band.Status.PUBLISHED)


class PublishedAlbumManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(ready=Album.Status.PUBLISHED)


class Genre(ModelMixinData, models.Model):
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']

    name = models.CharField(max_length=100, verbose_name='Жанр')
    slug = models.SlugField(max_length=100, verbose_name='Слаг', unique=True)

    def get_absolute_url(self):
        return reverse('genre', kwargs={'genre_slug': self.slug})


class Tag(ModelMixinData, models.Model):
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']

    name = models.CharField(max_length=100, verbose_name='Тег')
    slug = models.SlugField(max_length=100, verbose_name='Слаг', unique=True)

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})


class Band(ModelMixinData, models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ['name']

    name = models.CharField(max_length=100, verbose_name='Группа')
    year = models.IntegerField(verbose_name='Год основания', validators=[MinValueValidator(1950),
                                                                         MaxValueValidator(datetime.now().year)])
    description = models.TextField(verbose_name='Описание')
    ready = models.BooleanField(verbose_name='Публикация', choices=tuple(map(lambda x: (bool(x[0]), x[1]),
                                                                             Status.choices)), default=Status.DRAFT)
    photo = models.ImageField(upload_to=band_directory_path, verbose_name='Изображение')
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT, verbose_name='Жанр', related_name='genre_status')
    tags = models.ManyToManyField(Tag, verbose_name='Теги', blank=True, related_name='tags_status')
    slug = models.SlugField(max_length=100, verbose_name='Слаг', unique=True, null=True, blank=True)

    objects = models.Manager()
    published = PublishedBandManager()

    def get_absolute_url(self):
        return reverse('band', kwargs={'band_slug': self.slug})


class Album(ModelMixinData, models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    class Meta:
        verbose_name = 'Альбом'
        verbose_name_plural = 'Альбомы'
        ordering = ['year']

    name = models.CharField(max_length=100, verbose_name='Альбом')
    year = models.IntegerField(verbose_name='Год издания', validators=[MinValueValidator(1950),
                                                                       MaxValueValidator(datetime.now().year)])
    band = models.ForeignKey(Band, verbose_name='Группа', on_delete=models.PROTECT, related_name='band_status')
    ready = models.BooleanField(verbose_name='Публикация', choices=tuple(map(lambda x: (bool(x[0]), x[1]),
                                                                             Status.choices)), default=Status.DRAFT)
    photo = models.ImageField(upload_to=album_directory_path, verbose_name='Изображение', blank=True, null=True)
    slug = models.SlugField(max_length=100, verbose_name='Слаг', unique=True, null=True, blank=True)

    objects = models.Manager()
    published = PublishedAlbumManager()

    def get_absolute_url(self):
        return reverse('album', kwargs={'album_slug': self.slug})


class Track(models.Model):
    class Meta:
        verbose_name = 'Трек'
        verbose_name_plural = 'Треки'
        ordering = ['album']

    name = models.CharField(max_length=100, verbose_name='Композиция')
    url_path = models.FileField(verbose_name='Путь', upload_to=track_directory_path)
    album = models.ForeignKey(Album, verbose_name='Альбом', on_delete=models.CASCADE, related_name='track_status')

    def __str__(self):
        return '{}'.format(self.name)
