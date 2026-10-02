from django.test import TestCase
from routing.models import FuelStation
class BasicTests(TestCase):
    def test_station_model(self):
        FuelStation.objects.create(truckstop_id="1",name="Test",city="Dallas",state="TX",retail_price="3.00")
        self.assertEqual(FuelStation.objects.count(),1)
