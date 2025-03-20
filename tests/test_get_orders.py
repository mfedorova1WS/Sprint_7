def test_get_orders(api_client):
    response = api_client.get_orders()
    assert response.status_code == 200
    assert isinstance(response.json()['orders'], list)