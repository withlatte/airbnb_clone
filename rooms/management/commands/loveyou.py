from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "loveyou will print i love you --times number"

    def add_arguments(self, parser):
        parser.add_argument(
            "--times", help="how many TIMES are you gonna say I love you?"
        )

    def handle(self, *args, **options):
        times = options.get("times")
        for t in range(0, int(times)):
            self.stdout.write(self.style.ERROR("I love you"))
