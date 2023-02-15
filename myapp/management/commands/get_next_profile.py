import time
from django.core.management import BaseCommand
from myapp import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        get_next_profile()

def get_next_profile():
    p1, _ = models.Profile.objects.get_or_create(uid=1)
    p2, _ = models.Profile.objects.get_or_create(uid=2)
    p3, _ = models.Profile.objects.get_or_create(uid=3)
    models.Interaction.objects.filter(initiator=p1, subject=p2).delete()
    models.Interaction.objects.filter(initiator=p1, subject=p3).delete()

    time.sleep(1)
    p2.update_activity()
    print('info', p2, p3)
    print(p1.get_next_profile())
    models.Interaction.objects.create(initiator=p1, subject=p2, result=True)

    time.sleep(1)
    p3.update_activity()
    print(p1.get_next_profile())
