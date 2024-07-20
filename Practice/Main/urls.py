from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainPage.as_view(), name='main'),
    path('genre/<slug:genre_slug>/', views.GenrePage.as_view(), name='genre'),
    path('band/<slug:band_slug>/', views.BandPage.as_view(), name='band'),
    path('album/<slug:album_slug>/', views.AlbumPage.as_view(), name='album'),
    path('tag/<slug:tag_slug>/', views.TagPage.as_view(), name='tag'),
    path('search/', views.SearchPage.as_view(), name='search'),
    path('add-band/', views.AddBandPage.as_view(), name='add_band'),
    path('add-album/', views.AddAlbumPage.as_view(), name='add_album'),
    path('success/', views.SuccessPage.as_view(), name='success'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
