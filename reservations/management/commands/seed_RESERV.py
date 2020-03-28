import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django_seed import Seed, seeder as mom_seeder
from users import models as user_models
from rooms import models as room_models
from reservations import models as reservation_models

NAME = "Reservations"

seeder = Seed.seeder()
in_day = date.today()
out_day = date.today()


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
        # seeder = Seed.seeder()
        son_seeder = Seeder(faker=True)

        all_users = user_models.User.objects.all()
        all_rooms = room_models.Room.objects.all()

        son_seeder.add_entity(
            reservation_models.Reservation,
            number,
            {
                "guest": lambda x: random.choice(all_users),
                "room": lambda x: random.choice(all_rooms),
                "check_in": son_seeder.in_date(),
                "check_out": son_seeder.out_date(in_day),
                # "check_in": lambda x: seeder.faker.date_between(
                #     start_date="-30d", end_date="today"
                # ),
                # "check_out": lambda x: seeder.faker.date_between(
                #     start_date="today", end_date="today"
                # )
                # + timedelta(days=random.randint(1, 31)),
            },
        )
        son_seeder.execute()

        self.stdout.write(
            self.style.NOTICE(f"{number} {NAME} are created successfully!")
        )


class Seeder(mom_seeder.Seeder):
    @staticmethod
    def in_date():
        in_day = seeder.faker.date_this_year(before_today=True, after_today=True)
        return in_day

    @staticmethod
    def out_date(in_day_arg):
        return in_day_arg + timedelta(days=random.randint(1, 31))
