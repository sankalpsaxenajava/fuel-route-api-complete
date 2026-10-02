import requests
from django.core.cache import cache
class RoutingError(Exception): pass
def get_route(sl,sa,fl,fa):
    k=f"route:{sa:.5f}:{sl:.5f}:{fa:.5f}:{fl:.5f}"; hit=cache.get(k)
    if hit:return hit
    coords=f"{sl},{sa};{fl},{fa}"
    r=requests.get(f"https://router.project-osrm.org/route/v1/driving/{coords}",params={"overview":"full","geometries":"geojson","steps":"false"},headers={"User-Agent":"fuel-route-assessment/1.0"},timeout=30); r.raise_for_status(); p=r.json()
    if p.get("code")!="Ok" or not p.get("routes"): raise RoutingError("No driving route found")
    x=p["routes"][0]; out={"distance_meters":x["distance"],"distance_miles":round(x["distance"]/1609.344,2),"duration_seconds":round(x["duration"]),"duration_minutes":round(x["duration"]/60,2),"geometry":x["geometry"]}; cache.set(k,out,86400); return out
