from django.contrib import admin
from myapp.models import Volunteer, Donation, ContactMessage, Profile

admin.site.register(Profile)
admin.site.register(Volunteer)
admin.site.register(Donation)
admin.site.register(ContactMessage)