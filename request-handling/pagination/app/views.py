import csv, math
from django.core.paginator import Paginator
from django.shortcuts import render_to_response, redirect
from django.urls import reverse
from django.conf import settings


def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):

    bus_stations_list = []

    with open(settings.BUS_STATION_CSV, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            bus_stations_list.append({
                'Name': row['Name'],
                'Street': row['Street'],
                'District': row['District']})

    paginator = Paginator(bus_stations_list, 10)
    current_page = request.GET.get('page')
    per_page_list = paginator.get_page(current_page)
    return render_to_response('index.html', {'bus_stations': per_page_list})