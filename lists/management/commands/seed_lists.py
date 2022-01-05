# python manage.py seed_lists --number [num]
import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from lists import models as lists_models
from users import models as users_models
from rooms import models as rooms_models


class Command(BaseCommand):
    help = "This command creates lists"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="How many times do you want to create?",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        users = users_models.User.objects.all()
        rooms = rooms_models.Room.objects.all()
        seeder.add_entity(
            lists_models.List,
            number,
            {
                "user": lambda x: random.choice(users),
            },
        )
        created = seeder.execute()
        cleaned = flatten(list(created.values()))

        for pk in cleaned:
            list_model = lists_models.List.objects.get(pk=pk)
            to_add = rooms[random.randint(0, 5) : random.randint(6, 30)]  # 슬라이싱
            list_model.rooms.add(*to_add)  # *to_add: 배열의 내용물을 저장하기 위해

        self.stdout.write(self.style.SUCCESS(f"{number} lists created!"))
