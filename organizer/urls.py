from django.urls import path

from . import views

urlpatterns = [
    path("events/auto_create", views.event_auto_add, name="event_auto_add"),
    path("events/<int:event_id>/", views.event_detail, name="event_detail"),
    path("events/<int:event_id>/tickets/", views.ticket_add, name="ticket_add"),
    path("venues/", views.venue_add, name="venue_add"),
]
