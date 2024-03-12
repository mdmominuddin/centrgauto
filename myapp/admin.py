from django.contrib import admin
from .models import Event, Participant, ParticipantEvent, CourseOffer, Country, OfficersandStaffs, upEvent

class EventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'host_country', 'start_date', 'end_date', 'total_days', 'govt_order')

admin.site.register(Event, EventAdmin)

class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('rank', 'name')

admin.site.register(Participant, ParticipantAdmin)

class ParticipantEventAdmin(admin.ModelAdmin):
    list_display = ('participant', 'event')

admin.site.register(ParticipantEvent, ParticipantEventAdmin)

class CourseOfferAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'ff_country', 'year')

admin.site.register(CourseOffer, CourseOfferAdmin)

class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'country_class')
    search_fields = ('name',)
    list_filter = ('country_class',)

admin.site.register(Country, CountryAdmin)

class OfficersandStaffsAdmin(admin.ModelAdmin):
    list_display = ('rank','name','designation')
    search_fields = ('rank','name','designation')
    list_filter = ('designation','staffstatus')
admin.site.register(OfficersandStaffs, OfficersandStaffsAdmin)

class upEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'date', 'start_time', 'end_time', 'created_at', 'updated_at')
    search_fields = ['title', 'location', ]
    list_filter = ['date', 'created_at', 'updated_at']

admin.site.register(upEvent, upEventAdmin)