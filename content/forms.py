from django import forms
from users.models import User
from django.core.validators import RegexValidator


class ClientMessageForm(forms.Form):


    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Введите корректный номер телефона (например, +79991234567)."
    )

    COMMUNICATION_CHOISES = (
        ("telegram", "telegram"),
        ("WhatsApp", "WhatsApp"),
        ("Email", "Email"),
        ("Phone", "Phone"),
    )

    # Добавляем поле с выбором в виде радиокнопок
    communication = forms.ChoiceField(
        choices=COMMUNICATION_CHOISES,
        widget=forms.RadioSelect(attrs={"class": "image-radio-input"}),  # Добавляем класс для JS/CSS
        label="Предпочтительный способ коммуникации",
        initial="Phone"

    )

    message = forms.CharField(
        label="Сообщение",
        widget=forms.Textarea(
            attrs={
                "class": "w-full px-5 py-2.5 text-base font-medium bg-transparent border rounded-md outline-none border-zink-800 dark:border-dark-3 text-zink-800 dark:text-dark-6 focus:border-pink-800 dark:focus:border-pink-800",
                "placeholder": "Отправить сообщение здесь",
                "rows": "5",
                "style": "height: 120px;",
            }
        ),
    )

    is_agree = forms.BooleanField(
        label="Я согласен на обработку персональных данных",
        widget=forms.CheckboxInput(
            attrs={
                "class": "w-4 h-4 text-pink-800 bg-zink-50 border-zink-800 rounded focus:ring-pink-800 cursor-pointer"
            }
        ),
        required=True
    )

    full_name = forms.CharField(
        label="Имя",
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-5 py-2.5 text-base font-medium bg-transparent border rounded-md outline-none border-zink-800 dark:border-dark-3 text-zink-800 dark:text-dark-6 focus:border-pink-800 dark:focus:border-pink-800",
                "placeholder": "Имя",
                "type": "text",
                "name": "name",
            }
        )
    )
    email = forms.EmailField(
        label="Email",
        required=False,
        widget=forms.EmailInput(
            attrs={
                "class": "w-full px-5 py-2.5 text-base font-medium bg-transparent border rounded-md outline-none text-zink-800 dark:border-dark-3 text-zink-800 dark:text-dark-6 focus:border-pink-800 dark:focus:border-pink-800",
                "placeholder": "Email",
                "type": "email",
                "name": "email",
            }
        )
    )
    phone = forms.CharField(
        label="Телефон",
        required=True,
        validators=[phone_validator],
        widget=forms.TelInput(
            attrs={
                "class": "w-full px-5 py-2.5 text-base font-medium bg-transparent border rounded-md outline-none text-zink-800 dark:border-dark-3 text-zink-800 dark:text-dark-6 focus:border-pink-800 dark:focus:border-pink-800",
                "placeholder": "Телефон",
                "type": "tel",
                "name": "phone"
            }
        )
    )
