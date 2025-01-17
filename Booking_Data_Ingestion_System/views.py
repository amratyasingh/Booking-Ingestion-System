from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from datetime import datetime, date
import json

date_format = "%d-%m-%Y"


def change_date_format(input_date):
    return str(input_date.strftime("%d/%m/%Y"))

def create_booking(request):
    if request.method == "POST":
        data = request.POST
        field_list = [
            "BookingId",
            "CustomerName",
            "BookingDate",
            "Amount",
            "VendorDetails"
        ]
        final_date = ""
        content = ""
        is_valid = True
        for i in field_list:
            if not data.get(i):
                content = "Missing field {}".format(i)
                is_valid = False
                break
            if i == "BookingDate":
                if not bool(datetime.strptime(data.get(i),date_format)):
                    content = "Date format is not valid"
                    is_valid = False
                else:
                    input_date = data.get(i).split("-")
                    final_date = datetime.date(input_date[2], input_date[1], input_date(0))
        if not is_valid:
            return HttpResponse(status=400, content=content)
        else:
            Booking.objects.create(
                booking_id = data["BookingId"], customer_name = data["CustomerName"],
                booking_date = final_date, amount = data["Amount"],
                vendor_name = data["VendorDetails"]
            )
            return HttpResponse(status=200, content="Successfully done the booking")
    elif request.method == "GET":
        data = request.GET
        input_date = data.get("BookingDate")
        vendor = data.get("VendorDetails")
        if input_date:
            if not bool(datetime.strptime(input_date,date_format)):
                content = "Date format is not valid"
                return HttpResponse(status=400, content=content)
            else:
                date_lst = input_date.split("-")
                bookings_data = Booking.objects.filter(
                    event_date__date=date(date_lst[2], date_lst[1], date_lst[0])).values()
        elif vendor: 
            bookings_data = Booking.objects.get(vendor_name=vendor).values()
        else:
            bookings_data = Booking.objects.all().values()
        if len(bookings_data) > 0:
            for booking_info in bookings_data:
                booking_info['booking_date'] = change_date_format(booking_info['booking_date'])
            final_data = {
                "bookings": bookings_data
            }
            content = json.dumps(final_data)
        else:
            content = "No record found"
        return HttpResponse(status=200, content=content)

def get_booking(request, id):
    if request.method == "GET":
        if id:
            bookings_data = Booking.objects.filter(booking_id=int(id)).values()
            if len(bookings_data) > 0:
                bookings_data = bookings_data[0]
                bookings_data['booking_date'] = change_date_format(bookings_data['booking_date'])
                final_data = {
                    "bookings": bookings_data
                }
                content=json.dumps(final_data)
            else:
                content = "Booking Id does not exist"
            return HttpResponse(status=200, content=content)


def delete_booking(request, id):
    if request.method == "GET":
        if id:
            try:
                bookings_data = Booking.objects.get(booking_id=id)
                bookings_data.delete()
                content = "Successfully deleted the booking having id {}".format(id)
            except Booking.DoesNotExist:
                content = "Booking Id does not exist"

            return HttpResponse(status=200, content=content)

