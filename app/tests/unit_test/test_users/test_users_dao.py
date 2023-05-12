import pytest
from app.users.dao import UsersDAO


@pytest.mark.parametrize("user_id, user_email, role, exist", [
    (1, "test@test.com", "user", True),
    (2, "artem@example.com", "user", True),
    (4, "fake@email.fk", "user", False),
])
async def test_find_user_by_id(user_id, user_email, role, exist):
    user = await UsersDAO.find_by_id(user_id)

    if exist:
        assert user
        assert user.email == user_email
        assert user.id == user_id
        assert user.role == role
    else:
        assert not user