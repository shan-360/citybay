from django.contrib import admin
from .models import Search, User, Registration, RateCity, DistinctRateCity

# Register your models here.

admin.site.register(Search)
admin.site.register(User)
admin.site.register(Registration)
admin.site.register(RateCity)
admin.site.register(DistinctRateCity)
