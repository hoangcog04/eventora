from typing import List

from django.db import transaction
from django.shortcuts import get_object_or_404

from common.constants.business import (
    DEFAULT_CHECKOUT_METHOD,
    DEFAULT_QUANTITY_LOCK,
    FIRST_TICKET_NAME,
    FIRST_TICKET_SORTING,
)
from common.constants.params import (
    CHECKOUT_SETTING_EXPANSION,
    PROPERTY_EXPANSION,
    VENUE_EXPANSION,
)

from ..models import (
    Agenda,
    Attribute,
    AttributeValue,
    CheckoutSetting,
    Event,
    Faq,
    Ticket,
    TicketStock,
)
from ..serializers.event import EventAddRes, EventDetail


@transaction.atomic
def auto_add_event(data) -> "EventAddRes":
    event_data = data.pop("event")
    ticket_data = data.pop("ticket")

    # mocking
    event_data["organizer_id"] = 1
    if ticket_data["price"] == 0:
        event_data["is_free"] = True
    event = Event.objects.create(**event_data)

    ticket_data["event_id"] = event.id
    ticket_data["name"] = FIRST_TICKET_NAME
    ticket_data["capacity"] = event.capacity
    ticket_data["sorting"] = FIRST_TICKET_SORTING
    ticket = Ticket.objects.create(**ticket_data)

    TicketStock(
        ticket=ticket,
        quantity_available=ticket.capacity,
        quantity_lock=DEFAULT_QUANTITY_LOCK,
    ).save()

    CheckoutSetting(event=event, checkout_method=DEFAULT_CHECKOUT_METHOD).save()

    return EventAddRes({"event": event, "ticket": ticket})


def get_event_detail(event_id: int, expand_list: List[str]) -> "EventDetail":
    event = get_object_or_404(Event, pk=event_id)

    attr_values = AttributeValue.objects.filter(event_id=event_id)

    if attr_values.exists():
        attribute_ids = attr_values.values_list("attribute_id", flat=True)
        attr = Attribute.objects.filter(id__in=attribute_ids)

    if VENUE_EXPANSION in expand_list:
        venue = event.venue

    checkout_settings = []
    if CHECKOUT_SETTING_EXPANSION in expand_list:
        checkout_settings = CheckoutSetting.objects.filter(event_id=event_id)

    agendas = []
    faqs = []
    if PROPERTY_EXPANSION in expand_list:
        agendas = Agenda.objects.filter(event_id=event_id)
        faqs = Faq.objects.filter(event_id=event_id)

    return EventDetail(
        {
            "event": event,
            "venue": venue,
            "attribute_values": attr_values,
            "attributes": attr,
            "checkout_settings": checkout_settings,
            "agendas": agendas,
            "faqs": faqs,
        }
    )
