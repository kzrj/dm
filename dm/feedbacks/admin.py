from django.contrib import admin

from feedbacks.models import Feedback, Suggestion


@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Suggestion._meta.fields]


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Feedback._meta.fields]