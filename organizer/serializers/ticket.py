from rest_framework import serializers

from organizer.models import Ticket


class TicketAddReq(serializers.ModelSerializer):
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

    def validate(self, data):
        data["is_free"] = True if data["price"] == 0 else False
        return data


class TicketAddRes(serializers.Serializer):
    class TicketRes(serializers.ModelSerializer):
        class Meta:
            model = Ticket
            fields = "__all__"

    class CostRes(serializers.ModelSerializer):
        currency = serializers.CharField(max_length=3)

        class Meta:
            model = Ticket
            fields = ["price", "currency"]

    ticket = TicketRes()
    cost = CostRes()
