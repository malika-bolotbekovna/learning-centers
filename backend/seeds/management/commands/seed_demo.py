# backend/seeds/management/commands/seed_demo.py
from django.core.management.base import BaseCommand
from user.models import User, Role
from core.models import Category, Center, Program

class Command(BaseCommand):
    help = "Seed demo data"

    def handle(self, *args, **kwargs):
        admin, _ = User.objects.get_or_create(
            username="admin",
            email="admin@example.com",
            defaults={"role": Role.ADMIN}
        )
        admin.set_password("Admin_12345")
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()

        cat_it, _ = Category.objects.get_or_create(name="Программирование", slug="programming")
        cat_art, _ = Category.objects.get_or_create(name="Рисование", slug="art")

        center, _ = Center.objects.get_or_create(
            name="Think&Code",
            city="Бишкек",
            address="ул. Пушкина, 15",
            phone="+996 555 000 111",
            website="https://example.com",
        )

        Program.objects.get_or_create(
            center=center,
            title="Python для начинающих",
            description="Основы Python",
            category=cat_it,
            topic="python",
            format="OFFLINE",
            price_min=3000,
            price_max=5000,
            schedule="Пн/Ср/Пт 18:00",
        )

        Program.objects.get_or_create(
            center=center,
            title="Digital-скетчинг",
            description="Основы иллюстрации",
            category=cat_art,
            topic="sketch",
            format="ONLINE",
            price_min=2000,
            price_max=4000,
            schedule="Сб/Вс 12:00",
        )

        self.stdout.write(self.style.SUCCESS("Demo data seeded"))
