from django.contrib import admin
from .models import Guest, Party


class GuestInline(admin.TabularInline):
    model = Guest
    fields = ('first_name', 'last_name', 'is_attending', 'meal')
    readonly_fields = ('first_name', 'last_name')


class PartyAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'category', 'rehearsal_dinner', 'is_attending')
    list_filter = ('type', 'category', 'is_attending', 'rehearsal_dinner')
    inlines = [GuestInline]


class GuestAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'party', 'is_attending', 'meal')
    list_filter = ('is_attending', 'meal', 'party__category', 'party__rehearsal_dinner')


admin.site.register(Party, PartyAdmin)
admin.site.register(Guest, GuestAdmin)
