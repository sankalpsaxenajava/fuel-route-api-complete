from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import FuelRouteRequestSerializer
from .services.geocoder import geocode_location,GeocodingError
from .services.router import get_route,RoutingError
from .services.fuel_planner import build_fuel_plan,FuelPlanningError
class HealthView(APIView):
    def get(self,request): return Response({"status":"ok"})
class FuelRouteView(APIView):
    def post(self,request):
        s=FuelRouteRequestSerializer(data=request.data); s.is_valid(raise_exception=True)
        try:
            start=geocode_location(s.validated_data["start"]); finish=geocode_location(s.validated_data["finish"])
            route=get_route(start["longitude"],start["latitude"],finish["longitude"],finish["latitude"])
            plan=build_fuel_plan(route)
        except (GeocodingError,RoutingError,FuelPlanningError) as e:
            return Response({"detail":str(e)},status=422)
        return Response({"start":start,"finish":finish,"route":route,"vehicle":{"maximum_range_miles":500,"miles_per_gallon":10},"fuel_plan":plan})
