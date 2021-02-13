from django.contrib import admin
from .models import Rawdata, Method, Psychotherapist

@admin.register(Rawdata)
class RawdataAdmin(admin.ModelAdmin):
    pass


@admin.register(Method)
class MethodAdmin(admin.ModelAdmin):
    pass


@admin.register(Psychotherapist)
class PsychotherapistAdmin(admin.ModelAdmin):
    pass
