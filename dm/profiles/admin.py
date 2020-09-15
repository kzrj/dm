from django.contrib import admin

from profiles.models import Profile, Contact


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Profile._meta.fields]


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Contact._meta.fields]
