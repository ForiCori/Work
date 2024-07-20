from django import forms
from django.core.exceptions import ValidationError

from .models import Band, Genre, Album


class AddBandForm(forms.ModelForm):
    genre = forms.ModelChoiceField(queryset=Genre.objects.all(), empty_label='Жанр', label='Жанр')

    class Meta:
        model = Band
        fields = ['name', 'genre', 'year', 'description', 'tags', 'photo']
        widgets = {
            'description': forms.Textarea(attrs={'cols': 50, 'rows': 5})
        }


class AddAlbumForm(forms.ModelForm):
    band = forms.ModelChoiceField(queryset=Band.published.all(), empty_label='Группа', label='Группа')

    class Meta:
        model = Album
        fields = ['name', 'year', 'band', 'photo']


class AddTrackForm(forms.Form):
    name_track = forms.CharField(max_length=100, label='Название',
                                 error_messages={'required': 'Поле не может быть пустым!'})
    url = forms.FileField(label='Путь')
