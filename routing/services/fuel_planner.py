from decimal import Decimal
from math import cos,radians
from shapely.geometry import LineString,Point
from django.conf import settings
from routing.models import FuelStation
MAX_RANGE=500.0; MPG=10.0
class FuelPlanningError(Exception): pass
def xy(lon,lat,origin): return (lon*69.172*cos(radians(origin)),lat*69.0)
def candidates(coords):
    if len(coords)<2: raise FuelPlanningError("Route geometry is incomplete")
    origin=sum(x[1] for x in coords)/len(coords); line=LineString([xy(a,b,origin) for a,b in coords]); out=[]
    for st in FuelStation.objects.filter(latitude__isnull=False,longitude__isnull=False).iterator():
        p=Point(xy(st.longitude,st.latitude,origin)); distance=line.distance(p)
        if distance<=settings.ROUTE_CORRIDOR_MILES: out.append((line.project(p),distance,st))
    return sorted(out,key=lambda x:x[0])
def station_dict(st): return {"id":st.id,"truckstop_id":st.truckstop_id,"name":st.name,"city":st.city,"state":st.state,"latitude":st.latitude,"longitude":st.longitude,"price_per_gallon":float(st.retail_price)}
def build_fuel_plan(route):
    distance=float(route["distance_miles"]); stations=candidates(route["geometry"]["coordinates"]); current=0.0; stops=[]; total=Decimal("0")
    while distance-current>MAX_RANGE:
        reachable=[x for x in stations if current<x[0]<=current+MAX_RANGE]
        if not reachable: raise FuelPlanningError("No reachable geocoded station within 500 miles; geocode more stations or use a longer route corridor")
        safe=[x for x in reachable if distance-x[0]<=MAX_RANGE or any(x[0]<y[0]<=x[0]+MAX_RANGE for y in stations)]
        chosen=min(safe or reachable,key=lambda x:(x[2].retail_price,-x[0])); mile,off,st=chosen; leg=mile-current; gallons=leg/MPG; cost=Decimal(str(gallons))*st.retail_price; total+=cost
        stops.append({"stop_number":len(stops)+1,"route_mile":round(mile,2),"distance_from_route_miles":round(off,2),"distance_from_previous_stop_miles":round(leg,2),"gallons_to_purchase":round(gallons,2),"estimated_cost":round(float(cost),2),"station":station_dict(st)})
        current=mile; stations=[x for x in stations if x[0]>current]
    final=distance-current
    price=Decimal(str(stops[-1]["station"]["price_per_gallon"])) if stops else (stations[0][2].retail_price if stations else Decimal("0")); total+=Decimal(str(final/MPG))*price
    return {"route_corridor_miles":settings.ROUTE_CORRIDOR_MILES,"fuel_stops":stops,"total_gallons_needed":round(distance/MPG,2),"total_fuel_cost":round(float(total),2),"currency":"USD","assumptions":["500-mile maximum range","10 MPG","fuel stations are pre-geocoded and filtered within the configured corridor"]}
