# Fuel Route API

Django REST API for USA route planning with cost-effective fuel stops. It uses Nominatim for geocoding, one OSRM driving-route call, the supplied CSV locally, and Shapely to find pre-geocoded stations within a route corridor. OSRM supports GeoJSON route geometry, and the public Nominatim service requires responsible throttling and a descriptive User-Agent.

## Setup

```bash
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
```

Copy the supplied attachment `fuel-prices-for-be-assessment.csv` into `data/`.

```bash
python manage.py import_fuel_prices data/fuel-prices-for-be-assessment.csv
```

Geocode stations once. For a quick demo, start with 100 or 200; every station is throttled to just over one request/second.

```bash
python manage.py geocode_stations --limit 200
```

Start the server:

```bash
python manage.py runserver
```

Health:
`GET http://127.0.0.1:8000/api/v1/health/`

Request:
`POST http://127.0.0.1:8000/api/v1/fuel-plan/`

```json
{"start":"Dallas, TX","finish":"Atlanta, GA"}
```

The response contains start/finish coordinates, route distance/duration, GeoJSON LineString, selected stops, gallons, prices, and total cost.

The algorithm projects stations onto the returned route in a local mile-based projection, keeps stations within 25 miles, and chooses the cheapest reachable station that keeps the remaining route feasible under a 500-mile range.

Run tests:
```bash
python manage.py test
```

For production, pre-geocode using a commercial/self-hosted geocoder or a trusted station coordinate source; do not bulk-call public Nominatim at runtime.
