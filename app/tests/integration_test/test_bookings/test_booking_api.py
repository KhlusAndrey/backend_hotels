import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "room_id, date_from, date_to, booked_rooms, status_code",
    [
        (4, "2030-05-01", "2030-05-10", 3, 200),
        (4, "2030-05-01", "2030-05-10", 4, 200),
        (4, "2030-05-01", "2030-05-10", 5, 200),
        (4, "2030-05-01", "2030-05-10", 6, 200),
        (4, "2030-05-01", "2030-05-10", 7, 200),
        (4, "2030-05-01", "2030-05-10", 8, 200),
        (4, "2030-05-01", "2030-05-10", 9, 200),
        (4, "2030-05-01", "2030-05-10", 10, 200),
        (4, "2030-05-01", "2030-05-10", 10, 409),
        (4, "2030-05-01", "2030-05-10", 10, 409),
        (4, "2030-05-10", "2030-05-09", 10, 409),
    ],
)
async def test_add_and_get_booking(
    room_id,
    date_from,
    date_to,
    status_code,
    booked_rooms,
    authentificated_ac: AsyncClient,
):
    response = await authentificated_ac.post(
        "/v1/bookings",
        params={"room_id": room_id, "date_from": date_from, "date_to": date_to},
    )

    assert response.status_code == status_code

    response = await authentificated_ac.get("/v1/bookings")

    assert len(response.json()) == booked_rooms


async def test_get_and_delete_all_bookings(authentificated_ac: AsyncClient):
    response = await authentificated_ac.get("/v1/bookings")
    # Was 2 in database and added 8
    assert len(response.json()) == 10
    # cheek deleting bookings
    for booking in response.json():
        response = await authentificated_ac.delete(f"/v1/bookings/{booking['id']}")
        assert response.status_code == 204
    response = await authentificated_ac.get("/v1/bookings")
    assert len(response.json()) == 0
