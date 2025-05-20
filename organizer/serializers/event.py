from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from common.constants.business import (
    DEFAULT_CHECKOUT_METHOD,
    DEFAULT_QUANTITY_LOCK,
    FIRST_TICKET_NAME,
    FIRST_TICKET_SORTING,
)

from ..models import CheckoutSetting, Event, Ticket, TicketStock, Venue


class AutoCreatePayload(serializers.Serializer):
    class EventIn(serializers.ModelSerializer):
        venue_id = serializers.IntegerField()

        class Meta:
            model = Event
            fields = [
                "venue_id",
                "title",
                "summary",
                "date",
                "start_time",
                "end_time",
                "capacity",
            ]

        def validate_venue_id(self, value):
            if not Venue.objects.filter(id=value).exists():
                raise serializers.ValidationError(
                    f"Venue with id {value} does not exist"
                )
            return value

        def validate_date(self, value):
            if value < timezone.now():
                raise serializers.ValidationError("Event date cannot be in the past")
            return value

        def validate(self, data):
            start = data["start_time"]
            end = data["end_time"]
            if start and end and start >= end:
                raise serializers.ValidationError("Finish must occur after start")
            return data

    class TicketIn(serializers.ModelSerializer):
        class Meta:
            model = Ticket
            fields = ["price", "max_quantity_per_order"]

        def validate(self, data):
            return data

    event = EventIn()
    ticket = TicketIn()

    @transaction.atomic
    def create(self, validated_data):
        event_data = validated_data.pop("event")
        ticket_data = validated_data.pop("ticket")

        # mocking
        event_data["organizer_id"] = 1
        if ticket_data["price"] == 0:
            event_data["is_free"] = True
            ticket_data["is_free"] = True
        event = Event.objects.create(**event_data)

        ticket_data["event_id"] = event.id
        ticket_data["name"] = FIRST_TICKET_NAME
        ticket_data["capacity"] = event.capacity
        ticket_data["sorting"] = FIRST_TICKET_SORTING
        ticket = Ticket.objects.create(**ticket_data)

        ticket_stock = TicketStock(
            ticket=ticket,
            quantity_available=ticket.capacity,
            quantity_lock=DEFAULT_QUANTITY_LOCK,
        )
        ticket_stock.save()

        checkout_setting = CheckoutSetting(
            event=event, checkout_method=DEFAULT_CHECKOUT_METHOD
        )
        checkout_setting.save()

        return AutoCreateRes({"event": event, "ticket": ticket})


class AutoCreateRes(serializers.Serializer):
    class EventOut(serializers.ModelSerializer):
        class Meta:
            model = Event
            fields = "__all__"

    class TicketOut(serializers.ModelSerializer):
        class Meta:
            model = Ticket
            fields = "__all__"

    event = EventOut()
    ticket = TicketOut()
