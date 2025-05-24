from typing import List


def parse_param(request) -> List[str]:
    expand = request.GET.get("expand", "")
    return expand.split(",") if expand else []
