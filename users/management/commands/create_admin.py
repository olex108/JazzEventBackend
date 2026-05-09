from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        super_user = User.objects.create(
            phone="+77777777777",
            email="oleksiy_mosiychuk@gmail.com",
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )
        super_user.set_password('1234qwer')
        super_user.save()