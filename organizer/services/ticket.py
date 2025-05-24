from django.db import transaction

from common.constants.business import DEFAULT_CHECKOUT_METHOD, DEFAULT_QUANTITY_LOCK
from organizer.models import CheckoutSetting, Ticket, TicketStock
from organizer.serializers.ticket import TicketAddRes


def _get_currency(event_id):
    try:
        checkout_setting = CheckoutSetting.objects.get(
            event_id=event_id, checkout_method=DEFAULT_CHECKOUT_METHOD
        )
        return checkout_setting.currency_code
    except CheckoutSetting.DoesNotExist:
        return "USD"


@transaction.atomic
def add_ticket(event_id: int, data) -> "TicketAddRes":
    data["event_id"] = event_id
    ticket = Ticket.objects.create(**data)

    TicketStock(
        ticket=ticket,
        quantity_available=ticket.capacity,
        quantity_lock=DEFAULT_QUANTITY_LOCK,
    ).save()

    currency = _get_currency(event_id)

    return TicketAddRes(
        {
            "ticket": ticket,
            "cost": {
                "price": ticket.price,
                "currency": currency,
            },
        }
    )
