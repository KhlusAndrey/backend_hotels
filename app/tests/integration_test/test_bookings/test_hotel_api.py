from datetime import date, datetime, timedelta

import pytest
from httpx import AsyncClient


async def test_get_all_hotels(authentificated_ac: AsyncClient):
    response = await authentificated_ac.get("/v1/hotels/all")

    assert response.status_code == 200
    assert len(response.json()) == 6


@pytest.mark.parametrize(
    "hotel_id, hotel_name, status_code",
    [
        (2, "Skala", 200),
        (3, "Hilton resort", 200),
    ],
)
async def test_get_hotels_by_id(
    hotel_id: int, hotel_name: str, status_code: int, authentificated_ac: AsyncClient
):
    response = await authentificated_ac.get(f"/v1/hotels/id?hotel_id={hotel_id}")
    assert response.status_code == status_code
    assert response.json()["name"] == hotel_name


current_date = datetime.today().date()
date_from = current_date + timedelta(days=1)
date_to = current_date + timedelta(days=4)


@pytest.mark.parametrize(
    "location, hotel_name, date_from, date_to, status_code, result",
    [
        ("Morocco", "Hilton resort", date_from, date_to, 200, True),
        ("Paris", "Hilton resort", date_from, date_to, 200, False),
    ],
)
async def test_get_hotels_by_location_and_dates(
    location: str,
    hotel_name: str,
    date_from: date,
    date_to: date,
    status_code: int,
    result: bool,
    authentificated_ac: AsyncClient,
):
    response = await authentificated_ac.get(
        f"/v1/hotels/{location}?date_from={date_from}&date_to={date_to}"
    )
    if not result:
        assert response.status_code == status_code
        assert response.json() == []
    else:
        assert response.status_code == status_code
        assert response.json()[0]["name"] == hotel_name
