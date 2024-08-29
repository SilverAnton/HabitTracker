from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email="cu-hawk@yandex.ru",
            first_name="New",
            last_name="User",
        )
        user.set_password("password123_new_user")
        user.save()
