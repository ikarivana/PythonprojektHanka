from django.contrib import admin
from viewer.models import (
    Pedikura, Rasy, Zdravi, Contact,
    PedikuraReview, RasyReview, ZdraviReview,
)

@admin.register(Pedikura)
class PedikuraAdmin(admin.ModelAdmin):
    list_display = ['name', 'procedure_time', 'price']
    search_fields = ['name', 'description']

@admin.register(Rasy)
class RasyAdmin(admin.ModelAdmin):
    list_display = ['name', 'procedure_time', 'price']
    search_fields = ['name', 'description']

@admin.register(Zdravi)
class ZdraviAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name', 'description']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email']
    search_fields = ['name', 'email', 'phone']

@admin.register(PedikuraReview)
class PedikuraReviewAdmin(admin.ModelAdmin):
    list_display = ['pedikura', 'review', 'rating', 'created', 'updated']
    list_filter = ['rating', 'created', 'updated']
    search_fields = ['pedikura__name', 'review__user__username', 'comment']

@admin.register(ZdraviReview)
class ZdraviReviewAdmin(admin.ModelAdmin):
    list_display = ['zdravi', 'review', 'rating', 'created', 'updated']
    list_filter = ['rating', 'created', 'updated']
    search_fields = ['zdravi__name', 'review__user__username', 'comment']

@admin.register(RasyReview)
class RasyReviewAdmin(admin.ModelAdmin):
    list_display = ['rasy', 'review', 'rating', 'created', 'updated']
    list_filter = ['rating', 'created', 'updated']
    search_fields = ['rasy__name', 'review__user__username', 'comment']
