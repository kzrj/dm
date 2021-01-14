from django.contrib import admin

from profiles.models import Profile, SocialLink


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Profile._meta.fields]


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = [f.name for f in SocialLink._meta.fields]