from aiohttp.web_request import Request
from aiohttp.web_fileresponse import FileResponse

from hack.config import INDEX_PATH


async def get_root(request: Request) -> FileResponse:  # noqa
    return FileResponse(INDEX_PATH)
