from django.test import TestCase
from datetime import datetime, timedelta
from myapp import models

# Create your tests here.

class UpdateClientsTest(TestCase):
    def setUp(self):
        self.p1, _ = models.Profile.objects.get_or_create(uid=1)
        self.p2, _ = models.Profile.objects.get_or_create(
            uid=2,
            defaults={'last_activity': datetime.today() - timedelta(days=1)}
        )
        self.p3, _ = models.Profile.objects.get_or_create(
            uid=3,
            defaults={'last_activity': datetime.today() - timedelta(days=1)}
        )

    def test_1(self):
        self.p2.update_activity()
        assert self.p2 == self.p1.get_next_profile()

        i = models.Interaction(initiator=self.p1, subject=self.p2, result=True)
        i.save()
        assert self.p3 == self.p1.get_next_profile()

        i = models.Interaction(initiator=self.p1, subject=self.p3, result=False)
        i.save()
        assert None == self.p1.get_next_profile()

        self.p2.profile_changed()
        assert self.p2 == self.p1.get_next_profile()
