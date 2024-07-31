from httpx import Client
import pytest

@pytest.mark.asyncio
async def test_health(client: Client):
    # pytest.set_trace()
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
