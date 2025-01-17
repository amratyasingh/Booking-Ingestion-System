from django.db import models

class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=100)
    booking_date = models.DateField()
    amount = models.IntegerField()
    vendor_name = models.CharField(max_length=150)