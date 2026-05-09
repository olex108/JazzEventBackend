from django.db import models

import re


class Keyword(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "ключевое слово"
        verbose_name_plural = "ключевые слова"
        ordering = ['-name']


class Instrument(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "инструмент"
        verbose_name_plural = "инструменты"
        ordering = ['name']


class LineUp(models.Model):
    title = models.CharField(verbose_name="Название состава", max_length=30)
    count = models.PositiveSmallIntegerField(verbose_name="Количество музыкантов")
    is_vocal = models.BooleanField(verbose_name="Вокал")
    image = models.ImageField(upload_to="line_up/image/", verbose_name="Фото")
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    price = models.PositiveIntegerField(verbose_name="Стоимость стандарт", null=True, blank=True)
    price_plus = models.PositiveIntegerField(verbose_name="Стоимость стандарт+", null=True, blank=True)
    price_premium = models.PositiveIntegerField(verbose_name="Стоимость премиум", null=True, blank=True)

    def __str__(self):
        vocal = "С вокалом" if self.is_vocal else "Без вокала"
        return f"{self.title} - {vocal}"

    class Meta:
        verbose_name = "состав"
        verbose_name_plural = "составы"
        ordering = ["count", "is_vocal"]


class LineUpComposition(models.Model):
    title = models.CharField(verbose_name="Название состава инструментов", max_length=200)
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    line_up = models.ForeignKey(LineUp, verbose_name="Состав", on_delete=models.CASCADE, related_name="line_up_composition")
    instruments = models.ManyToManyField(Instrument, verbose_name="Инструменты")

    def __str__(self):
        return f"{self.title} - {self.line_up}"

    class Meta:
        verbose_name = "состав инструментов"
        verbose_name_plural = "составы инструментов"
        ordering = ["title",]



class Event(models.Model):

    LINE_UP_CHOICES = (
        ("Соло", "соло"),
        ("Дуэт", "дует"),
        ("Трио", "трио"),
        ("Квартет", "квартет"),
        ("Группа", "группа"),
        ("Оркестр", "оркестр"),
    )

    title = models.CharField(max_length=300, verbose_name="Название")
    preview = models.ImageField(upload_to="event/preview/", verbose_name="Заставка", null=True, blank=True)
    video = models.ForeignKey(
        to="Video",
        # verbose_name="Главное видео",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="main_video_for_event"
    )
    description = models.TextField(verbose_name="Описание")
    date = models.DateField(verbose_name="Дата проведения", null=True, blank=True)

    line_up = models.CharField(max_length=12, choices=LINE_UP_CHOICES, verbose_name="Состав")
    is_vocal = models.BooleanField(default=False, verbose_name="Вокал")
    instruments = models.ManyToManyField(Instrument, verbose_name="Инструменты")

    keywords = models.ManyToManyField(Keyword, verbose_name="Ключевые слова")

    priority = models.PositiveIntegerField(default=1, verbose_name="Оценка приоритета")
    is_publicate = models.BooleanField(default=True, verbose_name="Публиковать")

    def __str__(self):
        return f"{self.title} - {self.date} - {self.line_up}"

    class Meta:
        verbose_name = "мероприятие"
        verbose_name_plural = "мероприятия"
        ordering = ["-priority", '-date']


class Image(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        verbose_name="Мероприятие",
        related_name="images",
        blank=True,
        null=True,
    )
    priority = models.PositiveSmallIntegerField(verbose_name="Оценка приоритета", default=1, null=True, blank=True)
    image = models.ImageField(upload_to="event/image/", verbose_name="Фото")

    def __str__(self):
        return f"{self.event} - {self.priority}"

    class Meta:
        verbose_name = "фото"
        verbose_name_plural = "фото"
        ordering = ['-priority']


class Video(models.Model):
    """
    Model of video from vk

    The video refers to the model Event
    Field priority helps the admin regulate the order in which videos are displayed by integer
    """

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        verbose_name="Мероприятие",
        related_name="videos",
        null=True,
        blank=True
    )
    priority = models.PositiveSmallIntegerField(verbose_name="Оценка приоритета", default=1, null=True, blank=True)
    preview = models.ImageField(upload_to="preview/video/", verbose_name="Заставка для видео", null=True, blank=True)

    # Меняем FileField на URLField
    video_url = models.URLField(
        verbose_name="Ссылка на видео ВК",
        help_text="Например: https://vk.com"
    )

    vk_hash = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Хэш (необязательно)",
        help_text="Если видео не грузится, скопируйте hash из кода экспорта"
    )

    def get_embed_url(self) -> str:
        """
        Converts a regular link to an iframe link.

        get pattern video-XXXX_XXXX
        """

        match = re.search(r"video(-?\d+)_(\d+)", self.video_url)

        if match:
            owner_id, video_id = match.groups()
            # Обрати внимание на /video_ext.php?oid=
            return f"https://vk.com/video_ext.php?oid={owner_id}&id={video_id}"

        return self.video_url

    def __str__(self) -> str:
        return f"{self.event} - Приоритет: {self.priority}"

    class Meta:
        verbose_name = "видео"
        verbose_name_plural = "видео"
        ordering = ['-priority']

# class VideoEvent(models.Model):
#
#     # If change the same must do in filters.py for correct work !!!
#     LINE_UP_CHOICES = (
#         ("SOLO", "соло"),
#         ("DUET", "дует"),
#         ("TRIO", "трио"),
#         ("QUARTET", "квартет"),
#         ("BAND", "группа"),
#         ("ORCHESTRA", "оркестр"),
#     )
#
#     title = models.CharField(max_length=300, verbose_name="Название")
#     preview = models.ImageField(upload_to="event/preview/", verbose_name="Заставка")
#     line_up = models.CharField(max_length=12, choices=LINE_UP_CHOICES, verbose_name="Состав")
#     is_vocal = models.BooleanField(default=False, verbose_name="Вокал")
#     description = models.TextField(verbose_name="Описание")
#     date = models.DateField(verbose_name="Дата проведения", null=True, blank=True)
#     keywords = models.ManyToManyField(Keyword, verbose_name="Ключевые слова")
#     priority = models.PositiveIntegerField(default=0, verbose_name="Оценка приоритета")
#     instruments = models.ManyToManyField(Instrument, verbose_name="Инструменты")
#
#     def __str__(self):
#         return f"{self.title} - {self.date}"
#
#     class Meta:
#         verbose_name = "мероприятие видео"
#         verbose_name_plural = "мероприятия видео"
#         ordering = ["-priority", '-date']
