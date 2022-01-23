from aiohttp.test_utils import TestClient

OK_STATUS = 'ok'


async def test_health(client: TestClient) -> None:
    resp = await client.get('/health')

    resp_data = await resp.json()

    assert resp.status == 200
    assert resp_data.get('status') == OK_STATUS
