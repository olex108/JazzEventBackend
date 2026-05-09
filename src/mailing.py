from django.core.mail import send_mail
import os
import logging


logger = logging.getLogger("messages")


class MailingService:

    @classmethod
    def send_welcome_client_email(cls, user_email: str) -> None:
        try:
            subject = "Jazz Event Russia"
            message = f"""Спасибо что обратились! Ваше сообщение принято, мы свяжемся Вами в ближайшее время"""
            from_email = os.getenv("EMAIL_ADDRESS")
            recipient_list = [user_email]
            send_mail(subject, message, from_email, recipient_list)
            logger.info(f"Send welcome email: {user_email}")
        except Exception as e:
            logger.error(f"Send welcome email: {user_email} | ERROR: {e}")

    @classmethod
    def send_email_new_message(cls, data: dict) -> None:
        """
        Функция для отправки сообщения для администратора сайта про новое обращение

        :data: Словарь с данными пользователя в виде
            {
                name: имя пользователя
                email: почта
                phone: телефон
                message: сообщение
                communication: предпочтительный способ коммуникации
            }
        """

        try:
            subject = "Новое обращение из сайта Jazz Event Russia!"
            message = f"""
                Получено новое обращение по форме сайта.
                Имя: {data["name"]}
                Email: {data["email"]}
                Телефон: {data["phone"]}
                Предпочтительный ответ на - {data["communication"]}
                
                {data["message"]}
            """
            from_email = os.getenv("EMAIL_ADDRESS")
            recipient_list = [data["email"],]
            send_mail(subject, message, from_email, recipient_list)
            logger.info(f"Send admin email: {data["email"]}")
        except Exception as e:
            logger.error(f"Send admin email: {data["email"]} | ERROR: {e}")
