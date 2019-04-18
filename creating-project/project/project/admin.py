from django.contrib import admin

# Register your models here.


from .models import Station, Route


class StationInline(admin.TabularInline):
    model = Station


class RouteInline(admin.TabularInline):
    model = Route


admin.site.register(Station)
admin.site.register(Route)
