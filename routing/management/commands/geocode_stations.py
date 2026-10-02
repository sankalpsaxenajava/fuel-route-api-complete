import time
from django.core.management.base import BaseCommand
from routing.models import FuelStation
from routing.services.geocoder import geocode_station
class Command(BaseCommand):
    def add_arguments(self,p): p.add_argument("--limit",type=int,default=None)
    def handle(self,*a,**o):
        qs=FuelStation.objects.filter(latitude__isnull=True).order_by("id")
        if o["limit"]: qs=qs[:o["limit"]]
        ok=fail=0
        for st in qs:
            try:
                rows=geocode_station(f"{st.name}, {st.city}, {st.state}, USA")
                if rows:
                    x=rows[0]; st.latitude=float(x["lat"]); st.longitude=float(x["lon"]); st.geocode_display_name=x.get("display_name","")[:500]; st.save(update_fields=["latitude","longitude","geocode_display_name"]); ok+=1
                else: fail+=1
            except Exception as e: fail+=1; self.stderr.write(str(e))
            time.sleep(1.05)
        self.stdout.write(self.style.SUCCESS(f"Geocoded={ok}, failed/not found={fail}"))
