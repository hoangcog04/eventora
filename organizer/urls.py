from django.urls import path

from . import views

urlpatterns = [
    path("events/auto_create", views.event_auto_create, name="auto_create"),
    path("events/<int:event_id>/", views.event_detail, name="event_detail"),
]
