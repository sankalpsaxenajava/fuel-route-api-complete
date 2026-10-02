import requests
from django.conf import settings
from django.core.cache import cache
NOMINATIM="https://nominatim.openstreetmap.org/search"
class GeocodingError(Exception): pass
def _search(q):
    r=requests.get(NOMINATIM,params={"q":q,"format":"jsonv2","limit":1,"countrycodes":"us"},headers={"User-Agent":settings.NOMINATIM_USER_AGENT},timeout=20); r.raise_for_status(); return r.json()
def geocode_location(q):
    k="geo:"+q.strip().lower(); hit=cache.get(k)
    if hit:return hit
    rows=_search(q)
    if not rows: raise GeocodingError(f"Location not found in USA: {q}")
    x=rows[0]; out={"query":q,"display_name":x.get("display_name",""),"latitude":float(x["lat"]),"longitude":float(x["lon"])}; cache.set(k,out,604800); return out
def geocode_station(q): return _search(q)
