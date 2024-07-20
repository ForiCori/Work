from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView

from .forms import AddBandForm, AddAlbumForm, AddTrackForm
from .models import Band, Album, Track
from .untils import TemplateMixinData


def main_page(request):
    records = Band.published.all()
    data = {
        'title': 'Test',
        'user': request.user.is_authenticated,
        'status': 0 if not request.user.is_authenticated else 1,
        'data_db': records
            }
    print(records)
    return render(request, 'main/index.html', data)


class MainPage(TemplateMixinData, ListView):
    template_name = 'main/index.html'
    context_object_name = 'data'
    title = 'Главная'

    def get_queryset(self):
        return Band.published.all()

    def get(self, request, *args, **kwargs):

        return super(MainPage, self).get(request, *args, **kwargs)


class GenrePage(TemplateMixinData, ListView):
    template_name = 'main/index.html'
    context_object_name = 'data'
    slug_url_kwarg = 'genre_slug'

    def get_queryset(self):
        # get_list_or_404(Band, genre__slug=self.kwargs['genre_slug'])
        return Band.published.filter(genre__slug=self.kwargs[self.slug_url_kwarg])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context['data']:
            select = context['data'][0].genre
            context['title'] = select.name
        else:
            context['title'] = 'Неизвестно'
        return context


class BandPage(TemplateMixinData, DetailView):
    # --------------model = Band + Album------------
    template_name = 'main/band.html'
    slug_url_kwarg = 'band_slug'
    context_object_name = 'data'

    def get_object(self, queryset=None):
        data = {'band': get_object_or_404(Band.published, slug=self.kwargs[self.slug_url_kwarg]),
                'albums': Album.published.filter(band__slug=self.kwargs[self.slug_url_kwarg])}
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['data']['band'].name
        return context


class AlbumPage(TemplateMixinData, DetailView):
    # --------------model = Album + Track------------
    template_name = 'main/album.html'
    slug_url_kwarg = 'album_slug'
    context_object_name = 'data'

    def get_object(self, queryset=None):
        data = {'album': get_object_or_404(Album.published, slug=self.kwargs[self.slug_url_kwarg]),
                'tracks': get_list_or_404(Track, album__slug=self.kwargs[self.slug_url_kwarg])}
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['data']['album'].name
        return context


class TagPage(TemplateMixinData, ListView):
    template_name = 'main/index.html'
    context_object_name = 'data'
    slug_url_kwarg = 'tag_slug'

    def get_queryset(self):
        return Band.published.filter(tags__slug=self.kwargs[self.slug_url_kwarg])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '#' + self.kwargs['tag_slug']
        context['tag'] = self.kwargs['tag_slug'].replace('-', ' ').capitalize()
        return context


class SearchPage(TemplateMixinData, ListView):
    template_name = 'main/index.html'
    context_object_name = 'data'
    title = 'Поиск'
    search = None

    def get(self, request, *args, **kwargs):
        if 'search' in request.GET:
            self.search = request.GET['search']
        return super(SearchPage, self).get(request, *args, **kwargs)

    def get_queryset(self):
        if self.search and len(self.search) > 3:
            return Band.published.filter(name__contains=self.search)
        else:
            return Band.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.search
        return context


class AddBandPage(LoginRequiredMixin, TemplateMixinData, CreateView):
    form_class = AddBandForm
    # model = --------------Band-----------
    # fields = ['__all__']
    template_name = 'main/add_band.html'
    success_url = reverse_lazy('success')
    title = 'Добавление группы'
    login_url = 'login'


class AddAlbumPage(LoginRequiredMixin, TemplateMixinData, TemplateView):
    # model = -------------Album + (Mult)Track ---------
    # fields = ['__all__']
    template_name = 'main/add_album.html'
    title = 'Добавление альбома'
    login_url = 'login'
    error = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_one'] = AddAlbumForm()
        context['form_two'] = AddTrackForm()
        context['error'] = self.error
        return context

    def post(self, request, *args, **kwargs):
        album_form = AddAlbumForm(request.POST, request.FILES)

        if album_form.is_valid():
            album_form.save()
            name_track = {x: request.POST[x] for x in request.POST if 'name_track' in x}
            url_track = {x: request.FILES[x] for x in request.FILES if 'url' in x}
            for name, url in zip(name_track, url_track):
                obj = Track(
                    name=name_track[name],
                    url_path=url_track[url],
                    album=Album.objects.get(name=album_form.cleaned_data['name'])
                )
                obj.save()
            return redirect('success')

        else:
            self.error = True
            return self.render_to_response(self.get_context_data())


class SuccessPage(TemplateMixinData, TemplateView):
    template_name = 'main/success.html'
    title = 'Уведомление'
