from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models_profile import Profile

class Command(BaseCommand):
    help = "Create profile for users who don't have one"

    def handle(self, *args, **options):
        count = 0
        for u in User.objects.all():
            p, created = Profile.objects.get_or_create(user=u)
            if created:
                count += 1
        self.stdout.write(self.style.SUCCESS(f"Profiles created: {count}"))
