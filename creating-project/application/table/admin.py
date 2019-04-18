from django.contrib import admin

# Register your models here.


from .models import TableSettings, PathToFile


class PathToFileInline(admin.TabularInline):
    model = PathToFile


class TableInline(admin.TabularInline):
    model = TableSettings


admin.site.register(PathToFile)
admin.site.register(TableSettings)
