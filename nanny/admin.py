from django.contrib import admin
from .models import pro_skills, Nanny, Location, Rate, Report

# Register your models here.
admin.site.register(pro_skills)
admin.site.register(Location)
admin.site.register(Nanny)
admin.site.register(Rate)
admin.site.register(Report)
