from logging import getLogger
from typing import Callable
from aiohttp.web_exceptions import HTTPNotFound
from aiohttp.web_middlewares import middleware
from aiohttp.web_request import Request
from aiohttp.web_response import Response

logger = getLogger(__name__)


@middleware
async def main_middleware(request: Request, handler: Callable) -> Response:
    try:
        return await handler(request)
    except HTTPNotFound:
        return Response(text='404 Page Not Found', status=404)
    except Exception:  # noqa
        logger.exception('Server error occurred')
        return Response(status=500)
