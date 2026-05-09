from users.models import User, ClientMessage
from users.services.user_services import UserServices
from django.db.models import F

import logging


logger = logging.getLogger("messages")


class ClientMessageServices:


    @staticmethod
    def create_client_message_obj(client: User, client_message: str, client_communication: str) -> ClientMessage:
        """
        Создание нового объекта модели ClientMessage.
        Создается заголовок.
        Создается новый объект.
        Создается и возвращается экземпляр класса ClientMessageServices
        """

        title = f"Сообщение он нового клиента - {client.full_name} - {client.phone} - {client_communication}"

        new_client_message = ClientMessage(
            client=client,
            title=title,
            message=client_message,
            communication=client_communication
        )
        new_client_message.save()

        return new_client_message

    @staticmethod
    def update_clint_message_obj(client: User, client_message: str, client_communication: str, client_email: str,
                                 client_full_name: str):
        """
        Статический метод проверяет у пользователя объекты ClientMessage
        Если да заменяется заголовок, дополняются поля message, comments новой информацией и меняется статус на NEW
        Если нет вызывается класс метод для создания нового ClientMessage
        """

        client_message_obj = ClientMessage.objects.filter(client=client).first()

        if client_message_obj:
            title = f"Повторное сообщение от клиента - {client.full_name} - {client.phone} - {client_communication}"
            old_message = client_message_obj.message
            new_message = f"""
                Новое сообщение:
                {client_message}
                Старое сообщение:
                {old_message}
            """
            old_comments = client_message_obj.comments
            new_comments = f"""
                При новом сообщении указаны:
                    Полное имя - {client_full_name}
                    Почта - {client_email}
                
                {old_comments}
            """

            client_message_obj.title=title
            client_message_obj.message=new_message
            client_message_obj.comments=new_comments
            client_message_obj.status=ClientMessage.NEW
            client_message_obj.communication=client_communication
            client_message_obj.save()

            return client_message_obj

        else:
            return ClientMessageServices.create_client_message_obj(client, client_message, client_communication)

    @staticmethod
    def add_comments(client_message_obj: ClientMessage, comments: str) -> None:

        old_comments = client_message_obj.comments
        new_comments = f"""
            {comments}

            {old_comments}
        """

        client_message_obj.comments=new_comments

        client_message_obj.save()
