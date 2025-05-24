from typing import List

from django.shortcuts import get_object_or_404

from common.constants.params import (
    CHECKOUT_SETTING_EXPANSION,
    PROPERTY_EXPANSION,
    VENUE_EXPANSION,
)

from ..models import Agenda, Attribute, AttributeValue, CheckoutSetting, Event, Faq
from ..serializers.event import EventDetail


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
