from users.models import User

import logging


logger = logging.getLogger("users")


class UserServices:
    full_name: str
    phone: str
    email: str

    def __init__(self, full_name: str, phone: str , email: str = None) -> None:

        self.full_name = full_name
        self.phone = phone
        self.email = email

        self.user, self.is_new_user = User.objects.get_or_create(
            full_name=full_name,
            phone=phone,
            email=email
        )

    def search_user(self) -> bool:

        return User.objects.filter(phone=self.phone).exists()

    def create_new_user(self) -> User:

        client = User(full_name=self.full_name, phone=self.phone, email=self.email)
        client.save()
        return client

    @staticmethod
    def get_or_save_client_by_phone(phone: str, full_name: str, email: str) -> User | None:
        """
        Method to get user by phone number or None
        """

        client = User.objects.filter(phone=phone).exists()
        if client:
            client.full_name = full_name
            if email:
                client.email = email
            client.save()
        else:
            client = User(full_name=full_name, phone=phone, email=email)
            client.save()
            logger.info(f"New client created: {phone}")

        return client
