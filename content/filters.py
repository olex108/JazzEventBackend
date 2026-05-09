import django_filters
from django import forms

from .models import Event, Instrument


class VideoFilter(django_filters.FilterSet):
    LINE_UP_CHOICES = Event.LINE_UP_CHOICES

    line_up = django_filters.ChoiceFilter(
        field_name="event__line_up",
        choices=LINE_UP_CHOICES,
        label="Составы",
        empty_label="Все"
    )

    instruments = django_filters.ModelMultipleChoiceFilter(
        field_name="event__instruments",
        queryset=Instrument.objects.all(),
        label="Инструменты",
        widget=forms.SelectMultiple(attrs={
            'class': 'ваши-css-классы',
            'id': 'multiSelectContainer'
        })
    )

    is_vocal = django_filters.BooleanFilter(
        field_name="event__is_vocal",
        label="Вокал"
    )

    class Meta:
        model = Event
        fields = []


class EventFilter(django_filters.FilterSet):
    LINE_UP_CHOICES = Event.LINE_UP_CHOICES

    line_up = django_filters.ChoiceFilter(
        choices=LINE_UP_CHOICES,
        label="Составы",
        empty_label="Все"
    )

    instruments = django_filters.ModelMultipleChoiceFilter(
        queryset=Instrument.objects.all(),
        label="Инструменты",
        widget=forms.SelectMultiple(attrs={
            'class': 'ваши-css-классы',
            'id': 'multiSelectContainer'
        })
    )

    is_vocal = django_filters.BooleanFilter(
        label="Вокал"
    )

    class Meta:
        model = Event
        fields = ["line_up", "instruments", "is_vocal"]