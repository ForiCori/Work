from django.contrib import admin
from Main.models import Genre, Tag, Band, Album, Track


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ['id', 'name', 'slug']
    list_display_links = ['id', 'name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ['id', 'name', 'slug']
    list_display_links = ['id', 'name']


@admin.register(Band)
class BandAdmin(admin.ModelAdmin):
    fields = ['name', 'year', 'description', 'ready', 'photo', 'genre', 'tags', 'slug']
    list_display = ['id', 'name', 'year', 'ready', 'slug']
    list_display_links = ['id', 'name']
    filter_horizontal = ['tags']
    list_editable = ['ready']
    search_fields = ['name']
    list_filter = ['ready']
    list_per_page = 20
    save_on_top = True


class TrackInline(admin.TabularInline):
    model = Track


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    fields = ['name', 'year', 'band', 'ready', 'photo', 'slug']
    list_display = ['id', 'name', 'year', 'band', 'ready', 'slug']
    list_display_links = ['id', 'name']
    list_editable = ['ready']
    search_fields = ['name']
    list_filter = ['ready', 'band']
    inlines = [TrackInline]
    list_per_page = 20
    save_on_top = True


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    fields = ['name', 'url_path', 'album', 'band_info']
    readonly_fields = ['band_info']
    list_display = ['id', 'name', 'album', 'band_info']
    list_display_links = ['id', 'name', 'album']
    search_fields = ['album']
    list_filter = ['album']
    list_per_page = 100
    save_on_top = True

    @admin.display(description='Группа')
    def band_info(self, track: Track):
        return track.album.band.name
