from httpx import AsyncClient
from faker import Faker
import pytest

fake = Faker()
test_email = fake.email()
test_password = fake.password()

@pytest.mark.parametrize("email,password,status_code",
    [
        (test_email, test_password, 200),  
        (test_email, test_password, 409),  
        ("not_email", "password", 422),
    ],
)
async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        })
    assert response.status_code == status_code


@pytest.mark.parametrize("email,password,status_code",
    [
        ("test@test.com", "wrong_password", 401),  
        ("wrong@email.com", "test", 401),
        ("wrong@email", "test", 422),
        ("test@test.com", "test", 200),  
    ],
)
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        })
    assert response.status_code == status_code