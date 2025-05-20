from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from common.adapters.result import success, validate_failed

from .serializers.event import AutoCreatePayload, AutoCreateRes


@extend_schema(request=AutoCreatePayload(), responses=AutoCreateRes())
@api_view(["POST"])
def auto_create(request):
    request = AutoCreatePayload(data=request.data, context={"request": request})
    if request.is_valid():
        response: AutoCreateRes = request.save()
        return Response(success(response.data), status=200)
    return Response(validate_failed(request.errors), status=400)
