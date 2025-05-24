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


class EventAddReq(serializers.Serializer):
    class EventReq(serializers.ModelSerializer):
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

    class TicketReq(serializers.ModelSerializer):
        class Meta:
            model = Ticket
            fields = ["price", "max_quantity_per_order"]

        def validate(self, data):
            data["is_free"] = True if data["price"] == 0 else False
            return data

    event = EventReq()
    ticket = TicketReq()


class EventAddRes(serializers.Serializer):
    class EventRes(serializers.ModelSerializer):
        class Meta:
            model = Event
            fields = "__all__"

    class TicketRes(serializers.ModelSerializer):
        class Meta:
            model = Ticket
            fields = "__all__"

    event = EventRes()
    ticket = TicketRes()


class EventDetail(serializers.Serializer):
    class EventRes(serializers.ModelSerializer):
        class Meta:
            model = Event
            exclude = ("capacity",)

    class VenueRes(serializers.ModelSerializer):
        class Meta:
            model = Venue
            exclude = ("organizer",)

    class AttrRes(serializers.ModelSerializer):
        class Meta:
            model = Attribute
            exclude = ("attribute_category",)

    class AttrValueRes(serializers.ModelSerializer):
        class Meta:
            model = AttributeValue
            exclude = ("event", "attribute_category")

    class CheckOutSettingRes(serializers.ModelSerializer):
        class Meta:
            model = CheckoutSetting
            fields = "__all__"

    class AgendaRes(serializers.ModelSerializer):
        class Meta:
            model = Agenda
            exclude = ("event",)

    class FaqRes(serializers.ModelSerializer):
        class Meta:
            model = Faq
            exclude = ("event",)

    event = EventRes()
    venue = VenueRes()
    attributes = AttrRes(many=True)
    attribute_values = AttrValueRes(many=True)
    checkout_settings = CheckOutSettingRes(many=True)
    agendas = AgendaRes(many=True)
    faqs = FaqRes(many=True)
