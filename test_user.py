import pytest
from sqlalchemy.exc import IntegrityError
from models import UserDatabase


@pytest.fixture
def user_db():
    # Setup: Create a temporary in-memory SQLite database
    db_url = "sqlite:///:memory:"
    db = UserDatabase(db_url)

    yield db  # This is where the testing happens

    # Teardown: Close the database connection
    db.close()


def test_add_user(user_db):
    user_db.add_user("john_doe", "john@example.com")
    user = user_db.get_user("john_doe")
    assert user is not None
    assert user.username == "john_doe"
    assert user.email == "john@example.com"


def test_get_nonexistent_user(user_db):
    user = user_db.get_user("nonexistent")
    assert user is None


def test_add_duplicate_user(user_db):
    user_db.add_user("jane_doe", "jane@example.com")
    with pytest.raises(IntegrityError):
        user_db.add_user("jane_doe", "jane_another@example.com")
