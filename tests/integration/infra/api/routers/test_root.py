async def test_health_check(client):
    response = await client.get("/health-check")
    data, status_code = response.json(), response.status_code
    assert status_code == 200
    assert data["status"] == "I'm ok!"
