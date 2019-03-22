import csv, math
from django.shortcuts import render_to_response, redirect
from django.urls import reverse
from app.settings import BUS_STATION_CSV


def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):

    bus_stations_list = []

    with open(BUS_STATION_CSV, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            bus_stations_list.append({
                'Name': row['Name'],
                'Street': row['Street'],
                'District': row['District']})

    bus_decade_count = math.ceil(len(bus_stations_list) / 10)
    current_page = 1
    prev_page_url = None
    next_page_url = None
    page_number = request.GET.get('page')
    if page_number:
        current_page = int(page_number)

    right = 10 * current_page
    if current_page == 1:
        left = 0
        if current_page != bus_decade_count:
            next_page_url = '?page=' + str((current_page + 1))

    else:
        left = right - 11
        prev_page_url = '?page=' + str((current_page - 1))
        if current_page != bus_decade_count:
            next_page_url = '?page=' + str((current_page + 1))

    bus_stations_list = bus_stations_list[left:right]
    return render_to_response('index.html', context={
        'bus_stations': bus_stations_list,
        'current_page': current_page,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
    })
