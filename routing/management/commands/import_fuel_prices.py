import csv,re
from decimal import Decimal
from django.core.management.base import BaseCommand
from routing.models import FuelStation
US={"AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY","DC"}
class Command(BaseCommand):
    def add_arguments(self,p): p.add_argument("file_path")
    def handle(self,*a,**o):
        FuelStation.objects.all().delete(); path=o["file_path"]; n=0
        with open(path,encoding="utf-8-sig",errors="ignore",newline="") as f:
            sample=f.read(4096); f.seek(0); dialect=csv.Sniffer().sniff(sample,delimiters=",\t|;")
            reader=csv.DictReader(f,dialect=dialect)
            for row in reader:
                keys={str(k).strip().lower().replace(" ","_"):v for k,v in row.items()}
                state=(keys.get("state") or keys.get("st") or "").strip().upper()
                if state not in US: continue
                def val(*names):
                    for name in names:
                        if keys.get(name): return str(keys[name]).strip()
                    return ""
                try: price=Decimal(val("retail_price","retail_price_per_gallon","price","fuel_price").replace("$",""))
                except Exception: continue
                sid=val("opis_truckstop_id","truckstop_id","id") or f"{val('truckstop_name','name')}:{val('city')}:{state}"
                city=val("city") or "Unknown"; name=val("truckstop_name","name","station_name") or "Fuel station"; address=val("address","location")
                obj,created=FuelStation.objects.get_or_create(truckstop_id=sid,city=city[:120],state=state,defaults={"name":name[:255],"address":address[:255],"retail_price":price})
                if not created and price<obj.retail_price: obj.retail_price=price; obj.save(update_fields=["retail_price"])
                n+=created
        self.stdout.write(self.style.SUCCESS(f"Imported {n} stations"))
