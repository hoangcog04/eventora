from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from common.adapters.result import success, validate_failed
from organizer.serializers.ticket import TicketAddIn, TicketAddOut
from organizer.serializers.venue import VenueSerializer
from organizer.services.event import auto_add_event, get_event_detail
from organizer.services.ticket import add_ticket
from organizer.services.venue import add_venue
from organizer.utils import parse_param

from .serializers.event import EventAddIn, EventAddOut, EventDetail


@extend_schema(request=EventAddIn(), responses=EventAddOut())
@api_view(["POST"])
def event_auto_add(request):
    serializer = EventAddIn(data=request.data)
    if serializer.is_valid():
        res = auto_add_event(serializer.validated_data)
        return Response(success(res.data), status=201)
    return Response(validate_failed(serializer.errors), status=400)


@extend_schema(responses=EventDetail())
@api_view(["GET"])
def event_detail(request, event_id):
    expand_list = parse_param(request)
    res = get_event_detail(event_id, expand_list)
    return Response(success(res.data), status=200)


@extend_schema(request=TicketAddIn(), responses=TicketAddOut())
@api_view(["POST"])
def ticket_add(request, event_id):
    serializer = TicketAddIn(data=request.data)
    if serializer.is_valid():
        res = add_ticket(event_id, serializer.validated_data)
        return Response(success(res.data), status=201)
    return Response(validate_failed(serializer.errors), status=400)


@extend_schema(request=VenueSerializer(), responses=VenueSerializer())
@api_view(["POST"])
def venue_add(request):
    serializer = VenueSerializer(data=request.data)
    if serializer.is_valid():
        res = add_venue(serializer.validated_data)
        return Response(success(res.data), status=201)
    return Response(validate_failed(serializer.errors), status=400)
