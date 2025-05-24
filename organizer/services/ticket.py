from django.db import transaction

from common.constants.business import DEFAULT_CHECKOUT_METHOD, DEFAULT_QUANTITY_LOCK
from organizer.models import CheckoutSetting, Ticket, TicketStock
from organizer.serializers.ticket import TicketAddOut


def _get_currency(event_id):
    try:
        checkout_setting = CheckoutSetting.objects.get(
            event_id=event_id, checkout_method=DEFAULT_CHECKOUT_METHOD
        )
        return checkout_setting.currency_code
    except CheckoutSetting.DoesNotExist:
        return "USD"


@transaction.atomic
def add_ticket(event_id: int, data) -> "TicketAddOut":
    data["event_id"] = event_id

    ticket = Ticket.objects.create(**data)

    ticket_stock = TicketStock(
        ticket=ticket,
        quantity_available=ticket.capacity,
        quantity_lock=DEFAULT_QUANTITY_LOCK,
    )
    ticket_stock.save()

    currency = _get_currency(event_id)

    return TicketAddOut(
        {
            "ticket": ticket,
            "cost": {
                "price": ticket.price,
                "currency": currency,
            },
        }
    )
