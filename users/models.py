from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    """
    Model of all users include clients
    """

    COMMUNICATION_CHOISES = [
        ("telegram", "telegram"),
        ("WhatsApp", "WhatsApp"),
        ("Email", "Email"),
        ("Phone", "Phone"),
    ]

    username = None
    phone = PhoneNumberField(unique=True, verbose_name="Телефон")
    email = models.EmailField(unique=True, verbose_name="Почта", blank=True, null=True)
    full_name = models.CharField(max_length=300, verbose_name="Полное имя", help_text="Полное имя")
    # personal fields
    first_name = models.CharField(max_length=300, verbose_name="Имя", help_text="Имя", null=True, blank=True)
    last_name = models.CharField(max_length=20, verbose_name="Фамилия", help_text="Фамилия", null=True, blank=True)
    mid_name = models.CharField(max_length=20, verbose_name="Отчество", help_text="Отчество", null=True, blank=True)
    birthday = models.DateField(verbose_name="День рождения", help_text="День рождения", null=True, blank=True)
    photo = models.ImageField(upload_to="users/avatar/", verbose_name="Фото", blank=True, null=True)
    # work fields
    communication = models.CharField(
        max_length=9,
        choices=COMMUNICATION_CHOISES,
        verbose_name="Способ коммуникации",
        default="Phone",
        null=True,
        blank=True,
    )
    company = models.CharField(
        max_length=30, verbose_name="Организация", help_text="Организация", null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    email_token = models.CharField(max_length=100, verbose_name="email token", blank=True, null=True)
    phone_token = models.CharField(max_length=100, verbose_name="phone token", blank=True, null=True)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.full_name} - {self.phone} - {self.email}"

    class Meta:
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"
        ordering = ["-updated_at"]


class ClientMessage(models.Model):
    """
    Model of all clients messages
    """

    NEW = "new"
    READ = "read"
    WORK = "work"
    DONE = "done"

    STATUS_CHOICES = [
        (NEW, "новое"),
        (READ, "прочитано"),
        (WORK, "в работе"),
        (DONE, "закрыто"),
    ]

    COMMUNICATION_CHOISES = [
        ("telegram", "telegram"),
        ("WhatsApp", "WhatsApp"),
        ("Email", "Email"),
        ("Phone", "Phone"),
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Имя клиента")
    title = models.CharField(max_length=300, verbose_name="Название", help_text="Название темы переписки")
    message = models.TextField(verbose_name="Сообщение", help_text="Введите сообщение")
    comments = models.TextField(
        verbose_name="Комментарии", help_text="Комментарии и примечания", null=True, blank=True
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, verbose_name="Статус", help_text="Статус сообщения", default=NEW
    )
    deadline_at = models.DateTimeField(verbose_name="Дата ответа", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    communication = models.CharField(
        max_length=9, choices=COMMUNICATION_CHOISES, verbose_name="Способ коммуникации", null=True, blank=True
    )

    def __str__(self):
        return f"{self.client} - {self.title} - {self.status} - {self.created_at} - {self.deadline_at} - {self.communication}"

    class Meta:
        verbose_name = "сообщение"
        verbose_name_plural = "сообщения"
        ordering = ["updated_at"]

class Message(models.Model):
    NEW = "new"
    READ = "read"

    STATUS_CHOICES = [
        (NEW, "новое"),
        (READ, "прочитано"),
    ]

    client_message = models.ForeignKey(ClientMessage, on_delete=models.CASCADE, verbose_name="Список сообщений", related_name="messages_list")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, verbose_name="Статус", help_text="Статус сообщения", default=NEW
    )
