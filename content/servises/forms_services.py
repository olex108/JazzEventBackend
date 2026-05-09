from users.models import ClientMessage

from content.forms import ClientMessageForm
from users.services.user_services import UserServices
from users.services.message_service import ClientMessageServices
from src.mailing import MailingService


class FormsServices:

    @staticmethod
    def handling_feedback_form(form: ClientMessageForm) -> ClientMessage:
        """
        Валидация формы при заполнении полей
        Если номера телефона нет в базе данных сохраняет нового клиента и сохраняет новое сообщение
        Если номер есть в базе данных сохраняется новое сообщение с комментариями в виде реквизитов клиента

        В случае указания почты пользователю отправляется сообщение

        Реализована функция уведомления администратора через почту

        Возвращает объект ClientMessage
        """

        client_full_name = form.cleaned_data["full_name"]
        client_phone = form.cleaned_data["phone"]
        client_email = form.cleaned_data["email"]

        client_message = form.cleaned_data["message"]
        is_agree_value = form.cleaned_data["is_agree"]
        client_communication = form.cleaned_data["communication"]

        client = UserServices(client_full_name, client_phone, client_email)

        if client.is_new_user:
            client_message_obj = ClientMessageServices.create_client_message_obj(client.user, client_message,
                                                                                 client_communication)
        else:
            client_message_obj = ClientMessageServices.update_clint_message_obj(client.user, client_message,
                                                                                client_communication, client_email,
                                                                                client_full_name)

        # Отправка сообщения пользователю в случае указания почты
        if client_email:
            MailingService.send_welcome_client_email(client_email)

        # Отправка сообщения администратору
        MailingService.send_email_new_message(
            {
                "name": client_full_name,
                "email": client_email,
                "phone": client_phone,
                "message": client_message,
                "communication": client_communication,
            }
        )

        return client_message_obj
