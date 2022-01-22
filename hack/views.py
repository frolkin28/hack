from aiohttp.web_request import Request
from aiohttp.web_fileresponse import FileResponse
from aiohttp.web_routedef import RouteTableDef
from hack.config import INDEX_PATH

routes = RouteTableDef()


@routes.get('/')
async def get_root(request: Request) -> FileResponse:  # noqa
    return FileResponse(INDEX_PATH)

@routes.get('/{tail:(?!api/)(.+)}/')
async def get_template(request: Request) -> FileResponse:
    return FileResponse(INDEX_PATH)