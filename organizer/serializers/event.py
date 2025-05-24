from django.utils import timezone
from rest_framework import serializers

from ..models import (
    Agenda,
    Attribute,
    AttributeValue,
    CheckoutSetting,
    Event,
    Faq,
    Ticket,
    Venue,
)


class EventAddIn(serializers.Serializer):
    class Event(serializers.ModelSerializer):
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

    class Ticket(serializers.ModelSerializer):
        class Meta:
            model = Ticket
            fields = ["price", "max_quantity_per_order"]

    event = Event()
    ticket = Ticket()


class EventAddOut(serializers.Serializer):
    class Event(serializers.ModelSerializer):
        class Meta:
            model = Event
            fields = "__all__"

    class Ticket(serializers.ModelSerializer):
        class Meta:
            model = Ticket
            fields = "__all__"

    event = Event()
    ticket = Ticket()


class EventDetail(serializers.Serializer):
    class Event(serializers.ModelSerializer):
        class Meta:
            model = Event
            exclude = ("capacity",)

    class Venue(serializers.ModelSerializer):
        class Meta:
            model = Venue
            exclude = ("organizer",)

    class Attr(serializers.ModelSerializer):
        class Meta:
            model = Attribute
            exclude = ("attribute_category",)

    class AttrValue(serializers.ModelSerializer):
        class Meta:
            model = AttributeValue
            exclude = ("event", "attribute_category")

    class CheckOutSetting(serializers.ModelSerializer):
        class Meta:
            model = CheckoutSetting
            fields = "__all__"

    class Agenda(serializers.ModelSerializer):
        class Meta:
            model = Agenda
            exclude = ("event",)

    class Faq(serializers.ModelSerializer):
        class Meta:
            model = Faq
            exclude = ("event",)

    event = Event()
    venue = Venue()
    attributes = Attr(many=True)
    attribute_values = AttrValue(many=True)
    checkout_settings = CheckOutSetting(many=True)
    agendas = Agenda(many=True)
    faqs = Faq(many=True)
