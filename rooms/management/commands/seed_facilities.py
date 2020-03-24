from django.core.management.base import BaseCommand
from rooms.models import Facility

"""
    def add_arguments(self, parser):
        parser.add_argument("poll_ids", nargs="+", type=int)
"""


class Command(BaseCommand):
    help = "Seed Facilities"

    def handle(self, *args, **options):
        facilities = [
            "Private entrance",
            "Paid parking on premises",
            "Paid parking off premises",
            "Elevator",
            "Parking",
            "Gym",
        ]

        for f in facilities:
            Facility.objects.create(name=f)

        self.stdout.write(
            self.style.SUCCESS(f"{len(facilities)} facilities created successfully!")
        )
