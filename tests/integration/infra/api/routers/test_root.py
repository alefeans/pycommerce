async def test_health_check(async_test_client):
    async with async_test_client as client:
        response = await client.get("/health-check")
    data, status_code = response.json(), response.status_code
    assert status_code == 200
    assert data["status"] == "I'm ok!"
