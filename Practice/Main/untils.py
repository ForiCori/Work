from pytils.translit import slugify

menu = [
    {'name': 'На главную', 'url_name': 'main'},
    {'name': 'Добавить группу', 'url_name': 'add_band'},
    {'name': 'Добавить альбом', 'url_name': 'add_album'},
]

login = [
    {'name': 'Войти', 'url_name': 'login'},
    {'name': 'Регистрация', 'url_name': 'registration'},
]


def band_directory_path(instance, filename):
    return 'band_screen/{}/{}'.format(instance.name, filename)


def album_directory_path(instance, filename):
    return 'albums/{}/{}/{}'.format(instance.band.name, instance.name, filename)


def track_directory_path(instance, filename):
    return 'albums/{}/{}/{}'.format(instance.album.band.name, instance.album.name, filename)


class ModelMixinData:
    dynamic = 'Группа', 'Альбом'

    @classmethod
    def validate(cls, arg):
        return arg in cls.dynamic

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.validate(self._meta.get_field('name').verbose_name):
            if self.ready and not self.slug:
                self.slug = slugify(self.name)
        else:
            self.slug = slugify(self.name)
        super().save(force_insert, force_update, using, update_fields)


class TemplateMixinData:
    paginate_by = 5
    title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main'] = menu[0]
        context['menu'] = menu[1:]
        context['login'] = login
        context['user'] = self.request.user
        if self.title:
            context['title'] = self.title
        return context
