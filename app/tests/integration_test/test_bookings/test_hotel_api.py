from datetime import datetime, timedelta
from httpx import AsyncClient
import pytest


async def test_get_all_hotels(authentificated_ac: AsyncClient):
    response = await authentificated_ac.get("/hotels/all")
    
    assert response.status_code == 200
    assert len(response.json()) == 6


@pytest.mark.parametrize("hotel_id, hotel_name, status_code", [
    (2, "Skala", 200),
    (3, "Hilton resort", 200),
])
async def test_get_hotels_by_id(hotel_id, hotel_name, status_code, authentificated_ac: AsyncClient):
    response = await authentificated_ac.get(f"/hotels/id?hotel_id={hotel_id}")
    assert response.status_code == status_code
    assert response.json()["name"] == hotel_name


current_date = datetime.today().date()
date_from = current_date + timedelta(days=1)
date_to = current_date + timedelta(days=4)

@pytest.mark.parametrize("location, hotel_name, date_from, date_to, status_code, result", [
    ("Morocco", "Hilton resort", date_from, date_to, 200, True),
    ("Paris", "Hilton resort", date_from, date_to, 200, False),
])
async def test_get_hotels_by_location_and_dates(location, hotel_name, date_from, date_to, status_code, result, authentificated_ac: AsyncClient):
    response = await authentificated_ac.get(f"hotels/{location}?date_from={date_from}&date_to={date_to}")
    if not result:
        assert response.status_code == status_code
        assert response.json() == []
    else:
        assert response.status_code == status_code
        assert response.json()[0]["name"] == hotel_name
