import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django_seed import Seed
from users import models as user_models
from rooms import models as room_models
from reservations import models as reservation_models

NAME = "Reservations"


class Command(BaseCommand):
    help = f"Seed {NAME}"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=1,
            type=int,
            help=f"How many times do you want to repeat to create {NAME}?",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()

        all_users = user_models.User.objects.all()
        all_rooms = room_models.Room.objects.all()

        seeder.add_entity(
            reservation_models.Reservation,
            number,
            {
                "guest": lambda x: random.choice(all_users),
                "room": lambda x: random.choice(all_rooms),
                "check_in": lambda x: seeder.faker.date_between(
                    start_date="-60d", end_date="-59d"
                ),
                "check_out": lambda x: seeder.faker.date_between(
                    start_date="-57d", end_date="-56d"
                )
                + timedelta(days=random.randint(1, 31)),
            },
        )
        seeder.execute()

        self.stdout.write(
            self.style.NOTICE(f"{number} {NAME} are created successfully!")
        )
