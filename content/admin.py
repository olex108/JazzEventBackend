from django.contrib import admin
from django.utils.html import format_html
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminBase # Добавьте SortableAdminBase

from .models import Event, Image, Keyword, Video, Instrument, LineUp, LineUpComposition


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)


@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(LineUp)
class LineUpAdmin(admin.ModelAdmin):
    list_display = ("count", "title", "is_vocal", "price", "price_premium")
    search_fields = ("count",)


@admin.register(LineUpComposition)
class LineUpCompositionAdmin(admin.ModelAdmin):
    list_display = ("title", "line_up", "instruments_list")
    search_fields = ("title", "line_up", "instruments")
    list_filter = ('line_up', "instruments")

    @admin.display(description="Инструменты")  # Заголовок колонки
    def instruments_list(self, obj):
        # Собираем имена всех связанных объектов в одну строку через запятую
        return ", ".join([item.name for item in obj.instruments.all()])


@admin.register(Image)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'event', 'priority')
    search_fields = ('event', 'priority')
    list_filter = ('event',)


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'event', 'priority', "video_url")
    search_fields = ('event', 'priority')
    list_filter = ('event',)


# 1. Инлайн для фотографий с Drag-and-Drop сортировкой
class ImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Image
    extra = 1
    # Показываем превью, само поле файла и скрываем число приоритета (оно меняется мышкой)
    fields = ('preview_tag', 'image', 'priority')
    readonly_fields = ('preview_tag',)

    # Красивое превью прямо в строке
    def preview_tag(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 70px; height: 45px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return "Нет фото"


# 2. Твой обновленный EventAdmin
@admin.register(Event)
class EventAdmin(SortableAdminBase, admin.ModelAdmin):  # SortableAdminBase ОБЯЗАТЕЛЕН
    list_display = ('id', 'title', 'date', 'priority', 'line_up')
    search_fields = ('title',)
    list_filter = ('line_up', 'date')

    # Сюда вставляем наши фото
    inlines = [ImageInline]

    class Media:
        css = {
            'all': ('https://cdnjs.cloudflare.com',)
        }
