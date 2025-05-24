from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from common.adapters.result import success, validate_failed
from organizer.services.event import get_event_detail
from organizer.utils import parse_param

from .serializers.event import AutoCreatePayload, AutoCreateRes, EventDetail


@extend_schema(request=AutoCreatePayload(), responses=AutoCreateRes())
@api_view(["POST"])
def event_auto_create(request):
    request = AutoCreatePayload(data=request.data)
    if request.is_valid():
        response: AutoCreateRes = request.save()
        return Response(success(response.data), status=200)
    return Response(validate_failed(request.errors), status=400)


@extend_schema(responses=EventDetail())
@api_view(["GET"])
def event_detail(request, event_id):
    expand_list = parse_param(request)
    res = get_event_detail(event_id, expand_list)
    return Response(success(res.data), status=200)
