from rest_framework import serializers

from organizer.models import Ticket


class TicketAddIn(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            "name",
            "summary",
            "pic",
            "price",
            "capacity",
            "max_quantity_per_order",
            "sorting",
            "is_free",
            "is_hidden",
        ]

    def validate(self, attrs):
        if attrs.get("price") == 0:
            attrs["is_free"] = True
        else:
            attrs["is_free"] = False
        return attrs


class TicketAddOut(serializers.Serializer):
    class Ticket(serializers.ModelSerializer):
        class Meta:
            model = Ticket
            fields = "__all__"

    class Cost(serializers.ModelSerializer):
        currency = serializers.CharField(max_length=3)

        class Meta:
            model = Ticket
            fields = ["price", "currency"]

    ticket = Ticket()
    cost = Cost()
