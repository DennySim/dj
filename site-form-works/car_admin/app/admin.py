from django.contrib import admin

from .models import Car, Review
from .forms import ReviewAdminForm, CarAdminForm


class CarAdmin(admin.ModelAdmin):
    form = CarAdminForm
    list_display = ('brand', 'model', 'review_count')
    pass


class ReviewAdmin(admin.ModelAdmin):
    form = ReviewAdminForm
    list_display = ('title', 'car')
    list_filter = ('title', 'car')
    search_fields = ('title', 'car__brand', 'car__model',)


admin.site.register(Car, CarAdmin)
admin.site.register(Review, ReviewAdmin)
