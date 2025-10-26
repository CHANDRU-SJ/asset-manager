import pytest
from datetime import date

@pytest.mark.asyncio(loop_scope="session")
async def test_create_asset(client):
    payload = {
        "name": "MacBook Pro",
        "category": "Electronics",
        "purchase_date": str(date.today()),
        "serial_number": "SN-12345"
    }
    response = await client.post("/assets/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "MacBook Pro"
    assert "id" in data


@pytest.mark.asyncio(loop_scope="session")
async def test_list_assets(client):
    response = await client.get("/assets/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert "id" in data[0]


@pytest.mark.asyncio(loop_scope="session")
async def test_get_asset_by_id(client):
    # create one first
    payload = {
        "name": "Dell XPS 13",
        "category": "Electronics",
        "purchase_date": str(date.today()),
        "serial_number": "SN-98765"
    }
    create = await client.post("/assets/", json=payload)
    asset_id = create.json()["id"]

    response = await client.get(f"/assets/{asset_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == asset_id


@pytest.mark.asyncio(loop_scope="session")
async def test_update_asset(client):
    # create first
    payload = {
        "name": "HP Laptop",
        "category": "Electronics",
        "purchase_date": str(date.today()),
        "serial_number": "SN-11111"
    }
    create = await client.post("/assets/", json=payload)
    asset_id = create.json()["id"]
    
    update_data = {"name": "HP EliteBook"}
    response = await client.put(f"/assets/{asset_id}", json=update_data)
    
    assert response.status_code == 200
    assert response.json()["name"] == "HP EliteBook"


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_asset(client):
    # create first
    payload = {
        "name": "To Delete",
        "category": "Misc",
        "purchase_date": str(date.today()),
        "serial_number": "SN-DEL"
    }
    create = await client.post("/assets/", json=payload)
    asset_id = create.json()["id"]

    response = await client.delete(f"/assets/{asset_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "deleted"
