from django.contrib import admin
from .models import Category, Event, Registration

# TODO: Register Category, Event, and Registration.
admin.site.register(Category)
admin.site.register(Event)
admin.site.register(Registration)