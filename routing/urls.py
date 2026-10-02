from django.urls import path
from .views import HealthView,FuelRouteView
urlpatterns=[path("health/",HealthView.as_view()),path("fuel-plan/",FuelRouteView.as_view())]
