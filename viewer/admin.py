from django.contrib import admin

from viewer.models import Pedikura, Rasy, Zdravi, Contact, PedikuraReview, ZdraviReview, RasyReview


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

admin.site.register(Pedikura)
admin.site.register(Rasy)
admin.site.register(Zdravi)
admin.site.register(Contact)
