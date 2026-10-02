from django.db import models
class FuelStation(models.Model):
    truckstop_id=models.CharField(max_length=50,db_index=True)
    name=models.CharField(max_length=255)
    address=models.CharField(max_length=255,blank=True)
    city=models.CharField(max_length=120)
    state=models.CharField(max_length=2,db_index=True)
    retail_price=models.DecimalField(max_digits=8,decimal_places=4,db_index=True)
    latitude=models.FloatField(null=True,blank=True,db_index=True)
    longitude=models.FloatField(null=True,blank=True,db_index=True)
    geocode_display_name=models.CharField(max_length=500,blank=True)
    class Meta:
        constraints=[models.UniqueConstraint(fields=["truckstop_id","city","state"],name="unique_station_location")]
        indexes=[models.Index(fields=["latitude","longitude"]),models.Index(fields=["state","city"])]
