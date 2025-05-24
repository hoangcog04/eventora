from django.db import transaction

from organizer.models import Venue
from organizer.serializers.venue import VenueSerializer


@transaction.atomic
def add_venue(data) -> VenueSerializer:
    data["organizer_id"] = 2
    venue = Venue.objects.create(**data)
    return VenueSerializer(venue)
